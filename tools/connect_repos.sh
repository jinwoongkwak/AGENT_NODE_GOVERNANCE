#!/usr/bin/env bash
# Reconnect sync-excluded repository folders to their remotes.
# Never pulls, pushes, merges, stashes, cleans, or rewrites work files.
set -u

LAUNCHER_NAME="Connect_Repo.sh"
ROOT_LAUNCHER_NAME="Connect_Repos.sh"
MARK_STREAM="com.dropbox.ignored"

usage() {
  cat <<'EOF'
Usage: connect_repos.sh --root DIR --manifest FILE [options]

  --root DIR            Workspace root that manifest paths are relative to.
  --manifest FILE       Tab-separated list: path, remote, branch, optional config (k=v;k=v).
  --repo PATH           Only process this manifest path. Repeatable.
  --apply               Connect missing .git, fetch, set sync-exclude marks and exclude entries.
                        Without it the tool only reports and changes nothing.
  --install-launchers   With --apply, write Connect_Repos.sh at the root and Connect_Repo.sh
                        in every existing repository folder.
  -h, --help            Show this help.
EOF
}

ROOT=""
MANIFEST=""
APPLY=0
INSTALL=0
FILTERS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="${2:-}"; shift 2 ;;
    --manifest) MANIFEST="${2:-}"; shift 2 ;;
    --repo) FILTERS+=("${2:-}"); shift 2 ;;
    --apply) APPLY=1; shift ;;
    --install-launchers) INSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [ -z "$ROOT" ] || [ -z "$MANIFEST" ]; then usage >&2; exit 2; fi
if ! ROOT="$(cd "$ROOT" 2>/dev/null && pwd)"; then echo "ERROR root not found" >&2; exit 2; fi
if [ ! -f "$MANIFEST" ]; then echo "ERROR manifest not found: $MANIFEST" >&2; exit 2; fi
MANIFEST="$(cd "$(dirname "$MANIFEST")" && pwd)/$(basename "$MANIFEST")"
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

N_OK=0; N_CONNECTED=0; N_INFO=0; N_WARN=0; N_SKIP=0; N_FAIL=0

report() {
  local state="$1" path="$2" msg="$3"
  case "$state" in
    OK) N_OK=$((N_OK + 1)) ;;
    CONNECTED) N_CONNECTED=$((N_CONNECTED + 1)) ;;
    INFO) N_INFO=$((N_INFO + 1)) ;;
    WARN) N_WARN=$((N_WARN + 1)) ;;
    SKIP) N_SKIP=$((N_SKIP + 1)) ;;
    FAIL) N_FAIL=$((N_FAIL + 1)) ;;
  esac
  printf '%-11s %s\n            %s\n' "[$state]" "$path" "$msg"
}

to_win() { cygpath -w "$1" 2>/dev/null || printf '%s' "$1"; }

# Sync-exclude marks are NTFS alternate data streams, which bash cannot write, so PowerShell handles them.
# Prints "<had-mark>\t<has-mark-now>\t<windows-path>" per path. Returns 1 if any path is unmarked afterwards.
dropbox_marks() {
  local mode="$1"; shift
  [ $# -eq 0 ] && return 0
  if ! command -v powershell.exe >/dev/null 2>&1; then
    echo "powershell.exe not found"
    return 1
  fi
  local list p out rc
  list="$(mktemp)"
  for p in "$@"; do to_win "$p"; printf '\n'; done > "$list"
  out="$(DBX_LIST="$(to_win "$list")" DBX_MODE="$mode" DBX_STREAM="$MARK_STREAM" \
    powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command '
      $ProgressPreference = "SilentlyContinue"
      function Test-Mark($p) {
        try { $null = Get-Content -LiteralPath $p -Stream $env:DBX_STREAM -ErrorAction Stop; return $true } catch { return $false }
      }
      $bad = 0
      foreach ($p in [IO.File]::ReadAllLines($env:DBX_LIST, [Text.Encoding]::UTF8)) {
        if (-not $p) { continue }
        $had = Test-Mark $p
        if (-not $had -and $env:DBX_MODE -eq "apply") {
          try { Set-Content -LiteralPath $p -Stream $env:DBX_STREAM -Value 1 -ErrorAction Stop } catch {}
        }
        $now = Test-Mark $p
        if (-not $now) { $bad = 1 }
        "{0}`t{1}`t{2}" -f $had, $now, $p
      }
      exit $bad' 2>&1)"
  rc=$?
  rm -f "$list"
  printf '%s\n' "$out" | tr -d '\r'
  return $rc
}

ensure_exclude() {
  local dir="$1" gitdir exclude
  gitdir="$(git -C "$dir" rev-parse --absolute-git-dir 2>/dev/null)" || return 0
  exclude="$gitdir/info/exclude"
  mkdir -p "$gitdir/info"
  if ! grep -qxF "/$LAUNCHER_NAME" "$exclude" 2>/dev/null; then
    printf '/%s\n' "$LAUNCHER_NAME" >> "$exclude"
  fi
}

apply_config() {
  local dir="$1" config="$2" item key value
  [ -z "$config" ] && return 0
  local IFS=';'
  for item in $config; do
    [ -z "$item" ] && continue
    key="${item%%=*}"; value="${item#*=}"
    git -C "$dir" config "$key" "$value" || return 1
  done
}

submodule_paths() {
  local dir="$1"
  [ -s "$dir/.gitmodules" ] || return 0
  git -C "$dir" config -f .gitmodules --get-regexp '^submodule\..*\.path$' 2>/dev/null |
    while read -r key subpath; do
      printf '%s\t%s\n' "${key%.path}" "$subpath"
    done
}

submodule_pointer_files() {
  local dir="$1" name subpath
  while IFS=$'\t' read -r name subpath; do
    [ -e "$dir/$subpath/.git" ] && printf '%s\n' "$dir/$subpath/.git"
  done < <(submodule_paths "$dir")
}

# Prints notes on success; on failure prints the reason and returns 1.
restore_submodules() {
  local dir="$1" name subpath url sha sub notes=""
  while IFS=$'\t' read -r name subpath; do
    sub="$dir/$subpath"
    [ -e "$sub/.git" ] && continue
    if [ ! -d "$sub" ] || [ -z "$(ls -A "$sub" 2>/dev/null)" ]; then
      notes="$notes 하위 모듈 $subpath: 파일 없음(초기화 안 함)."
      continue
    fi
    url="$(git -C "$dir" config -f .gitmodules --get "$name.url")"
    sha="$(git -C "$dir" ls-tree HEAD -- "$subpath" | awk '$2 == "commit" {print $3}')"
    if [ -z "$url" ] || [ -z "$sha" ]; then
      notes="$notes 하위 모듈 $subpath: 주소나 기록된 커밋이 없어 건너뜀."
      continue
    fi
    mkdir "$sub/.git" || { echo "하위 모듈 $subpath: .git 생성 실패"; return 1; }
    dropbox_marks apply "$sub/.git" >/dev/null || { echo "하위 모듈 $subpath: Dropbox 제외 표시 실패"; return 1; }
    { git -C "$sub" init -q &&
      git -C "$sub" remote add origin "$url" &&
      git -C "$sub" fetch -q origin; } || { echo "하위 모듈 $subpath: fetch 실패"; return 1; }
    git -C "$sub" cat-file -e "$sha^{commit}" 2>/dev/null || { echo "하위 모듈 $subpath: 기록된 커밋 $sha 없음"; return 1; }
    { git -C "$sub" update-ref --no-deref HEAD "$sha" &&
      git -C "$sub" reset -q &&
      git -C "$dir" submodule --quiet init -- "$subpath" &&
      git -C "$dir" submodule --quiet absorbgitdirs -- "$subpath"; } || { echo "하위 모듈 $subpath: 구조 복원 실패"; return 1; }
    dropbox_marks apply "$sub/.git" >/dev/null || { echo "하위 모듈 $subpath: 포인터 파일 제외 표시 실패"; return 1; }
    notes="$notes 하위 모듈 $subpath: 기록된 커밋 ${sha:0:7}에 연결."
  done < <(submodule_paths "$dir")
  printf '%s' "$notes"
}

state_summary() {
  local dir="$1" branch counts dirty
  branch="$(git -C "$dir" symbolic-ref -q --short HEAD)"
  dirty="$(git --no-optional-locks -C "$dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  if counts="$(git -C "$dir" rev-list --left-right --count 'HEAD...@{u}' 2>/dev/null)"; then
    set -- $counts
    printf '브랜치 %s, 원격보다 앞섬 %s·뒤처짐 %s, 변경 파일 %s' "${branch:-(detached)}" "$1" "$2" "$dirty"
  else
    printf '브랜치 %s, upstream 없음, 변경 파일 %s' "${branch:-(detached)}" "$dirty"
  fi
}

connect_new() {
  local dir="$1" path="$2" remote="$3" branch="$4" config="$5" out current notes=""

  if [ ! -e "$dir/.git" ]; then
    mkdir "$dir/.git" || { report FAIL "$path" ".git 폴더를 만들지 못함"; return; }
  fi
  if ! out="$(dropbox_marks apply "$dir/.git")"; then
    report FAIL "$path" "Dropbox 제외 표시 실패, git 초기화를 멈춤: $out"
    return
  fi
  git -C "$dir" init -q -b "$branch" 2>/dev/null || git -C "$dir" init -q ||
    { report FAIL "$path" "git init 실패"; return; }
  apply_config "$dir" "$config" || { report FAIL "$path" "config 적용 실패: $config"; return; }

  if current="$(git -C "$dir" remote get-url origin 2>/dev/null)"; then
    if [ "$current" != "$remote" ]; then
      report FAIL "$path" "기존 origin($current)이 목록($remote)과 다름. 바꾸지 않음"
      return
    fi
  else
    git -C "$dir" remote add origin "$remote" || { report FAIL "$path" "origin 추가 실패"; return; }
  fi

  if ! git -C "$dir" fetch -q origin; then
    report FAIL "$path" "fetch 실패(네트워크·권한 확인). .git은 남겨두었고 다시 실행하면 이어서 진행"
    return
  fi
  if ! git -C "$dir" rev-parse -q --verify "refs/remotes/origin/$branch" >/dev/null; then
    report FAIL "$path" "원격에 브랜치 $branch 없음"
    return
  fi

  if ! { git -C "$dir" update-ref "refs/heads/$branch" "refs/remotes/origin/$branch" &&
         git -C "$dir" symbolic-ref HEAD "refs/heads/$branch" &&
         git -C "$dir" reset -q &&
         git -C "$dir" branch -q --set-upstream-to="origin/$branch" "$branch"; }; then
    report FAIL "$path" "브랜치 연결 실패"
    return
  fi

  if grep -qs 'filter=lfs' "$dir/.gitattributes"; then
    git -C "$dir" lfs install --local >/dev/null 2>&1 || notes=" LFS hook 설치 실패(git-lfs 확인)."
  fi
  ensure_exclude "$dir"

  if ! out="$(restore_submodules "$dir")"; then
    report FAIL "$path" "원격 연결은 됐지만 $out"
    return
  fi
  report CONNECTED "$path" "$(state_summary "$dir"). 변경 파일은 Dropbox로 받은 파일과 원격 브랜치의 차이이니 확인하세요.${notes}${out}"
}

check_existing() {
  local dir="$1" path="$2" remote="$3" branch="$4" state="OK" msgs="" current now out p
  local marks=()

  current="$(git -C "$dir" remote get-url origin 2>/dev/null)"
  if [ "$current" != "$remote" ]; then
    state="WARN"; msgs="$msgs origin이 목록과 다름(현재 ${current:-없음}, 목록 $remote). 바꾸지 않음."
  fi

  now="$(git -C "$dir" symbolic-ref -q --short HEAD)"
  if [ -z "$now" ]; then
    state="WARN"; msgs="$msgs detached HEAD: 작업 전 git switch <branch>."
  elif [ "$now" != "$branch" ] && [ "$state" = "OK" ]; then
    state="INFO"; msgs="$msgs 목록 브랜치($branch)와 다른 브랜치에서 작업 중."
  fi

  marks=("$dir/.git")
  while IFS= read -r p; do marks+=("$p"); done < <(submodule_pointer_files "$dir")
  if [ "$APPLY" -eq 1 ]; then
    if ! out="$(dropbox_marks apply "${marks[@]}")"; then
      state="WARN"; msgs="$msgs Dropbox 제외 표시 실패: $(printf '%s' "$out" | tr '\n' ' ')"
    fi
    ensure_exclude "$dir"
    if [ -n "$current" ] && ! git -C "$dir" fetch -q origin 2>/dev/null; then
      state="WARN"; msgs="$msgs fetch 실패(네트워크·권한 확인)."
    fi
  else
    if ! dropbox_marks check "${marks[@]}" >/dev/null; then
      state="WARN"; msgs="$msgs Dropbox 제외 표시 없음(--apply로 설정)."
    fi
    msgs="$msgs fetch 안 함."
  fi

  report "$state" "$path" "$(state_summary "$dir").$msgs"
}

process_repo() {
  local path="$1" remote="$2" branch="$3" config="$4"
  local dir="$ROOT/$path"

  if [ ! -d "$dir" ] || [ -z "$(ls -A "$dir" 2>/dev/null)" ]; then
    report SKIP "$path" "폴더가 없거나 비어 있음. Dropbox 동기화가 끝난 뒤 다시 실행하세요."
    return
  fi
  if [ -e "$dir/.git" ] && git -C "$dir" rev-parse -q --verify HEAD >/dev/null 2>&1; then
    check_existing "$dir" "$path" "$remote" "$branch"
  elif [ "$APPLY" -eq 1 ]; then
    connect_new "$dir" "$path" "$remote" "$branch" "$config"
  elif [ -e "$dir/.git" ]; then
    report WARN "$path" "연결이 끝나지 않은 .git이 있음. --apply로 다시 실행하면 이어서 진행."
  else
    report WARN "$path" ".git 없음. --apply로 원격($remote, $branch)에 연결."
  fi
}

write_if_changed() {
  local target="$1" content="$2"
  if [ ! -f "$target" ] || [ "$(cat "$target")" != "$content" ]; then
    printf '%s\n' "$content" > "$target"
  fi
}

install_launchers() {
  local tool_rel manifest_rel root_content repo_content path remote branch config dir
  tool_rel="${SCRIPT_PATH#"$ROOT"/}"
  manifest_rel="${MANIFEST#"$ROOT"/}"
  root_content="#!/usr/bin/env bash
# Double-click before work: reconnect every repository in $manifest_rel to its remote.
# It fetches but never pulls or pushes. Generated by $tool_rel --install-launchers.
root=\"\$(cd \"\$(dirname \"\${BASH_SOURCE[0]}\")\" && pwd)\"
bash \"\$root/$tool_rel\" --root \"\$root\" --manifest \"\$root/$manifest_rel\" --apply \"\$@\"
status=\$?
if [ -t 0 ]; then read -r -p \"Enter 키를 누르면 닫힙니다. \" _; fi
exit \$status"
  repo_content="#!/usr/bin/env bash
# Double-click before work: reconnect only this folder's repository to its remote.
# It fetches but never pulls or pushes. Generated by $tool_rel --install-launchers.
here=\"\$(cd \"\$(dirname \"\${BASH_SOURCE[0]}\")\" && pwd)\"
d=\"\$here\"
while [ \"\$d\" != \"/\" ] && [ ! -f \"\$d/$ROOT_LAUNCHER_NAME\" ]; do d=\"\$(dirname \"\$d\")\"; done
if [ ! -f \"\$d/$ROOT_LAUNCHER_NAME\" ]; then
  echo \"$ROOT_LAUNCHER_NAME 파일을 찾지 못했습니다.\"
  if [ -t 0 ]; then read -r -p \"Enter 키를 누르면 닫힙니다. \" _; fi
  exit 1
fi
exec bash \"\$d/$ROOT_LAUNCHER_NAME\" --repo \"\${here#\"\$d\"/}\""

  write_if_changed "$ROOT/$ROOT_LAUNCHER_NAME" "$root_content"
  echo "launcher: $ROOT_LAUNCHER_NAME"
  while IFS=$'\t' read -r path remote branch config || [ -n "${path:-}" ]; do
    path="${path%$'\r'}"
    case "$path" in ''|'#'*|path) continue ;; esac
    dir="$ROOT/$path"
    [ -d "$dir" ] || continue
    write_if_changed "$dir/$LAUNCHER_NAME" "$repo_content"
    [ -e "$dir/.git" ] && ensure_exclude "$dir"
    echo "launcher: $path/$LAUNCHER_NAME"
  done < "$MANIFEST"
}

normalize() { local p="${1//\\//}"; p="${p%/}"; printf '%s' "$p"; }

if [ "$INSTALL" -eq 1 ]; then
  if [ "$APPLY" -ne 1 ]; then echo "ERROR --install-launchers needs --apply" >&2; exit 2; fi
  install_launchers
  echo
fi

if [ "$APPLY" -eq 1 ]; then mode_label="연결 모드"; else mode_label="점검 모드, 변경 없음"; fi
echo "저장소 연결 점검 ($mode_label)"
echo "root: $ROOT"
echo

matched=()
while IFS=$'\t' read -r path remote branch config || [ -n "${path:-}" ]; do
  path="${path%$'\r'}"; remote="${remote:-}"; remote="${remote%$'\r'}"
  branch="${branch:-}"; branch="${branch%$'\r'}"; config="${config:-}"; config="${config%$'\r'}"
  case "$path" in ''|'#'*|path) continue ;; esac
  if [ "${#FILTERS[@]}" -gt 0 ]; then
    hit=0
    for f in "${FILTERS[@]}"; do [ "$(normalize "$f")" = "$path" ] && hit=1; done
    [ "$hit" -eq 1 ] || continue
    matched+=("$path")
  fi
  if [ -z "$remote" ] || [ -z "$branch" ]; then
    report FAIL "$path" "목록에 remote 또는 branch가 비어 있음"
    continue
  fi
  process_repo "$path" "$remote" "$branch" "$config"
done < "$MANIFEST"

for f in "${FILTERS[@]}"; do
  found=0
  for m in "${matched[@]}"; do [ "$(normalize "$f")" = "$m" ] && found=1; done
  [ "$found" -eq 1 ] || report FAIL "$(normalize "$f")" "목록에 없는 경로"
done

echo
echo "합계: OK $N_OK · CONNECTED $N_CONNECTED · INFO $N_INFO · WARN $N_WARN · SKIP $N_SKIP · FAIL $N_FAIL"
echo "기기를 바꾸기 전에는 커밋을 push하세요. stash와 원격에 없는 브랜치는 이 기기의 .git에만 남습니다."
[ "$N_FAIL" -eq 0 ]
