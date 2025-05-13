import os
import subprocess
import re

def generate_readme_with_links(output_dir, readme_path="README.md"):
    """
    diff_results 디렉토리의 결과물을 README.md 파일에 링크로 추가합니다.
    
    Args:
        output_dir: 결과가 저장된 디렉토리 경로
        readme_path: README.md 파일 경로
    """
    if not os.path.exists(output_dir):
        print(f"결과 디렉토리 {output_dir}가 존재하지 않습니다.")
        return
    
    # 결과 파일 목록 가져오기
    result_files = [f for f in os.listdir(output_dir) if f.endswith('.md')]
    
    # 카테고리별로 파일 분류
    lib_files = sorted([f for f in result_files if f.startswith('lib_')])
    src_files = sorted([f for f in result_files if f.startswith('src_')])
    summary_files = sorted([f for f in result_files if f.endswith('_differences.md')])
    
    # README.md 파일 내용 생성
    readme_content = "# 코드 비교 결과\n\n"
    readme_content += "원본 코드와 온체인 코드 간의 비교 결과입니다.\n\n"
    
    # 요약 파일 링크 추가
    if summary_files:
        readme_content += "## 요약 보고서\n\n"
        for file in summary_files:
            file_path = os.path.join(output_dir, file)
            file_name = file.replace('.md', '')
            # 상대 경로로 링크 생성
            readme_content += f"- [{file_name}]({output_dir}/{file})\n"
        readme_content += "\n"
    
    # lib 파일 링크 추가
    if lib_files:
        readme_content += "## 라이브러리 비교 결과\n\n"
        for file in lib_files:
            if file in summary_files:
                continue
                
            file_path = os.path.join(output_dir, file)
            lib_name = file.replace('lib_', '').replace('.md', '')
            # 상대 경로로 링크 생성
            readme_content += f"- [{lib_name}]({output_dir}/{file})\n"
        readme_content += "\n"
    
    # src 파일 링크 추가
    if src_files:
        readme_content += "## 소스 코드 비교 결과\n\n"
        for file in src_files:
            if file in summary_files:
                continue
                
            file_path = os.path.join(output_dir, file)
            src_name = file.replace('src_', '').replace('.md', '')
            # 상대 경로로 링크 생성
            readme_content += f"- [{src_name}]({output_dir}/{file})\n"
        readme_content += "\n"
    
    # README.md 파일에 추가 정보
    readme_content += "## 비교 방법\n\n"
    readme_content += "이 비교 결과는 다음 명령어를 사용하여 생성되었습니다:\n\n"
    readme_content += "```bash\n"
    readme_content += "python diff-cantina-onchain.py\n"
    readme_content += "```\n\n"
    readme_content += "각 파일에는 다음 정보가 포함되어 있습니다:\n\n"
    readme_content += "- 디렉토리 트리 구조 (추가/삭제/수정된 파일 표시)\n"
    readme_content += "- 추가/삭제/수정된 파일 목록\n"
    readme_content += "- 파일 내용 차이 (diff 형식)\n"
    readme_content += "- 파일 비교 통계\n\n"
    
    # README.md 파일 저장
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"README.md 파일이 생성되었습니다: {os.path.abspath(readme_path)}")
    return readme_path

def get_directory_tree(path, prefix="", is_last=True, status="", exclude_dirs=None):
    """
    디렉토리 구조를 트리 형태의 문자열로 반환합니다.
    
    Args:
        path: 트리를 생성할 디렉토리 경로
        prefix: 현재 라인의 접두사 (들여쓰기 용도)
        is_last: 현재 항목이 부모 디렉토리의 마지막 항목인지 여부
        status: 파일/디렉토리의 상태 표시 (추가됨/삭제됨/수정됨/동일)
        exclude_dirs: 제외할 디렉토리 목록
    
    Returns:
        트리 구조의 문자열
    """
    if exclude_dirs is None:
        exclude_dirs = []
    
    if os.path.basename(path) in exclude_dirs:
        return ""
    
    output = []
    
    # 현재 아이템의 라인 추가
    basename = os.path.basename(path)
    
    if os.path.isdir(path):
        # 디렉토리인 경우 폴더 아이콘 사용
        symbol = "📁 "
    else:
        # 파일인 경우 파일 아이콘 사용
        symbol = "📄 "
    
    # 상태 표시 추가
    status_str = f" ({status})" if status else ""
    
    # 트리 라인 구성
    if is_last:
        output.append(f"{prefix}└── {symbol}{basename}{status_str}")
        new_prefix = prefix + "    "
    else:
        output.append(f"{prefix}├── {symbol}{basename}{status_str}")
        new_prefix = prefix + "│   "
    
    if os.path.isdir(path):
        # 디렉토리 내용 가져오기
        try:
            items = sorted(os.listdir(path))
            
            # 항목 순회하며 재귀적으로 트리 생성
            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last_item = (i == len(items) - 1)
                
                output.append(get_directory_tree(
                    item_path, 
                    new_prefix, 
                    is_last_item, 
                    "", 
                    exclude_dirs
                ))
        except PermissionError:
            output.append(f"{new_prefix}└── [권한 없음]")
        except Exception as e:
            output.append(f"{new_prefix}└── [오류: {str(e)}]")
    
    return "\n".join(output)

def build_comparison_tree(original_path, onchain_path, relative_path=""):
    """
    두 디렉토리를 비교하여 차이점을 표시한 트리 구조를 구축합니다.
    
    Args:
        original_path: 원본 디렉토리 경로
        onchain_path: 온체인 디렉토리 경로
        relative_path: 현재 상대 경로 (재귀 호출용)
        
    Returns:
        dict: 비교 결과가 담긴 트리 구조 사전
            {
                'name': 항목 이름,
                'type': 'file' 또는 'dir',
                'status': 'added', 'deleted', 'modified', 'identical', 또는 '',
                'children': 하위 항목 목록 (디렉토리인 경우)
            }
    """
    # 현재 경로
    current_original = os.path.join(original_path, relative_path) if relative_path else original_path
    current_onchain = os.path.join(onchain_path, relative_path) if relative_path else onchain_path
    
    # 트리 루트 노드 (디렉토리 이름)
    root_name = os.path.basename(current_original) if os.path.exists(current_original) else os.path.basename(current_onchain)
    tree = {
        'name': root_name,
        'type': 'dir',
        'status': '',
        'children': []
    }
    
    # 모든 파일과 디렉토리 목록 수집
    original_items = set()
    onchain_items = set()
    
    try:
        if os.path.exists(current_original) and os.path.isdir(current_original):
            original_items = set(os.listdir(current_original))
    except Exception as e:
        print(f"Error listing original directory {current_original}: {str(e)}")
    
    try:
        if os.path.exists(current_onchain) and os.path.isdir(current_onchain):
            onchain_items = set(os.listdir(current_onchain))
    except Exception as e:
        print(f"Error listing onchain directory {current_onchain}: {str(e)}")
    
    # 원본에만 있는 항목 (삭제됨)
    for item in sorted(original_items - onchain_items):
        item_path = os.path.join(current_original, item)
        item_rel_path = os.path.join(relative_path, item) if relative_path else item
        
        if os.path.isdir(item_path):
            # 재귀적으로 삭제된 디렉토리의 내용 추가
            subtree = build_comparison_tree(original_path, onchain_path, item_rel_path)
            subtree['status'] = 'deleted'
            tree['children'].append(subtree)
        else:
            tree['children'].append({
                'name': item,
                'type': 'file',
                'status': 'deleted'
            })
    
    # 온체인에만 있는 항목 (추가됨)
    for item in sorted(onchain_items - original_items):
        item_path = os.path.join(current_onchain, item)
        item_rel_path = os.path.join(relative_path, item) if relative_path else item
        
        if os.path.isdir(item_path):
            # 재귀적으로 추가된 디렉토리의 내용 추가
            subtree = build_comparison_tree(original_path, onchain_path, item_rel_path)
            subtree['status'] = 'added'
            tree['children'].append(subtree)
        else:
            tree['children'].append({
                'name': item,
                'type': 'file',
                'status': 'added'
            })
    
    # 양쪽에 모두 있는 항목
    for item in sorted(original_items.intersection(onchain_items)):
        item_original_path = os.path.join(current_original, item)
        item_onchain_path = os.path.join(current_onchain, item)
        item_rel_path = os.path.join(relative_path, item) if relative_path else item
        
        # 디렉토리인 경우 재귀적으로 비교
        if os.path.isdir(item_original_path) and os.path.isdir(item_onchain_path):
            subtree = build_comparison_tree(original_path, onchain_path, item_rel_path)
            tree['children'].append(subtree)
        # 파일인 경우 내용 비교
        elif os.path.isfile(item_original_path) and os.path.isfile(item_onchain_path):
            try:
                # git diff로 파일 내용 비교
                diff_cmd = ["git", "diff", "--no-index", "--quiet", item_original_path, item_onchain_path]
                result = subprocess.run(diff_cmd, capture_output=True, text=True)
                
                # 반환 코드 0은 차이가 없음, 1은 차이가 있음을 의미
                status = 'identical' if result.returncode == 0 else 'modified'
                
                tree['children'].append({
                    'name': item,
                    'type': 'file',
                    'status': status
                })
            except Exception as e:
                print(f"Error comparing files {item_rel_path}: {str(e)}")
                tree['children'].append({
                    'name': item,
                    'type': 'file',
                    'status': 'error'
                })
    
    return tree

def render_tree_to_markdown(tree, prefix="", is_last=True):
    """
    트리 구조를 마크다운 포맷의 트리로 변환합니다.
    
    Args:
        tree: 트리 구조 데이터
        prefix: 현재 라인의 접두사 (들여쓰기 용도)
        is_last: 현재 항목이 부모의 마지막 항목인지 여부
        
    Returns:
        마크다운 형식의 트리 문자열
    """
    output = []
    
    # 아이콘 선택
    icon = "📁 " if tree['type'] == 'dir' else "📄 "
    
    # 상태에 따른 표시
    status_map = {
        'added': '(추가됨)',
        'deleted': '(삭제됨)',
        'modified': '(수정됨)',
        'identical': '(동일)',
        'error': '(비교 실패)'
    }
    status_str = status_map.get(tree['status'], "")
    
    # 트리 라인 구성
    if is_last:
        output.append(f"{prefix}└── {icon}{tree['name']} {status_str}")
        new_prefix = prefix + "    "
    else:
        output.append(f"{prefix}├── {icon}{tree['name']} {status_str}")
        new_prefix = prefix + "│   "
    
    # 하위 항목이 있는 경우 재귀적으로 처리
    if 'children' in tree and tree['children']:
        for i, child in enumerate(tree['children']):
            is_last_child = (i == len(tree['children']) - 1)
            child_output = render_tree_to_markdown(child, new_prefix, is_last_child)
            output.append(child_output)
    
    return "\n".join(output)

def compare_folders(original_path, onchain_path, output_dir="diff_results", folder_type="lib"):
    """
    두 폴더의 내용을 비교하여 git diff 결과를 마크다운 파일로 저장합니다.
    
    Args:
        original_path: 원본 폴더 경로
        onchain_path: 비교할 온체인 폴더 경로
        output_dir: diff 결과를 저장할 디렉토리
        folder_type: 폴더 유형 (lib 또는 src)
    """
    # 결과 저장할 디렉토리 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # 하위 디렉토리 목록 가져오기
    original_dirs = set(os.listdir(original_path))
    onchain_dirs = set(os.listdir(onchain_path))
    
    # 공통 디렉토리, 원본에만 있는 디렉토리, 온체인에만 있는 디렉토리
    common_dirs = original_dirs.intersection(onchain_dirs)
    only_original_dirs = original_dirs - onchain_dirs
    only_onchain_dirs = onchain_dirs - original_dirs
    
    # 한쪽에만 있는 디렉토리 기록
    if only_original_dirs or only_onchain_dirs:
        with open(os.path.join(output_dir, f"{folder_type}_differences.md"), 'w') as f:
            f.write(f"# {folder_type.upper()} 디렉토리 차이점 요약\n\n")
            
            if only_original_dirs:
                f.write("## 삭제된 디렉토리 목록\n\n")
                f.write(f"다음 디렉토리들은 원본에만 존재하고 온체인 버전에서는 삭제되었습니다:\n\n")
                for dir_name in sorted(only_original_dirs):
                    f.write(f"- `{dir_name}`\n")
                f.write("\n")
            
            if only_onchain_dirs:
                f.write("## 추가된 디렉토리 목록\n\n")
                f.write(f"다음 디렉토리들은 온체인 버전에만 존재하고 원본에는 없습니다:\n\n")
                for dir_name in sorted(only_onchain_dirs):
                    f.write(f"- `{dir_name}`\n")
                f.write("\n")
    
    # 각 하위 디렉토리별로 diff 실행
    for dir_name in common_dirs:
        original_dir_full_path = os.path.join(original_path, dir_name)
        onchain_dir_full_path = os.path.join(onchain_path, dir_name)
        
        # 폴더가 아닌 경우 스킵
        if not (os.path.isdir(original_dir_full_path) and os.path.isdir(onchain_dir_full_path)):
            continue
        
        print(f"Comparing {folder_type}/{dir_name}...")
        output_file = os.path.join(output_dir, f"{folder_type}_{dir_name}.md")
        
        # 마크다운 파일 헤더 작성
        with open(output_file, 'w') as f:
            f.write(f"# {folder_type}/{dir_name} 비교 결과\n\n")
            f.write(f"원본 경로: `{original_dir_full_path}`\n\n")
            f.write(f"온체인 경로: `{onchain_dir_full_path}`\n\n")
            
            # 디렉토리 트리 추가
            f.write("## 디렉토리 트리 구조\n\n")
            f.write("```\n")
            comparison_tree = build_comparison_tree(original_dir_full_path, onchain_dir_full_path)
            tree_md = render_tree_to_markdown(comparison_tree)
            f.write(tree_md)
            f.write("\n```\n\n")
            
            f.write("## 차이점\n\n")
        
        # 파일 목록 비교
        compare_files_in_directory(original_dir_full_path, onchain_dir_full_path, output_file, dir_name)
        
        # git diff 명령어 실행
        try:
            diff_cmd = ["git", "diff", "--no-index", original_dir_full_path, onchain_dir_full_path]
            diff_result = subprocess.run(diff_cmd, capture_output=True, text=True)
            
            # git diff는 차이가 있으면 exit code 1을 반환하므로 에러 처리 필요
            diff_output = diff_result.stdout if diff_result.stdout else diff_result.stderr
            
            # 결과가 없으면 "차이 없음" 메시지 기록
            if not diff_output or "exit status" in diff_output:
                with open(output_file, 'a') as f:
                    f.write("두 디렉토리 간 내용 차이가 없습니다.\n")
                print(f"No differences found for {folder_type}/{dir_name}")
                continue
            
            # 경로 정보 수정 (절대 경로를 상대 경로로 변환)
            modified_output = diff_output.replace(original_dir_full_path, f"{folder_type}/{dir_name} (원본)")
            modified_output = modified_output.replace(onchain_dir_full_path, f"{folder_type}/{dir_name} (온체인)")
            
            # 출력 결과를 마크다운 코드 블록으로 포맷팅
            with open(output_file, 'a') as f:
                f.write("### 파일 내용 차이\n\n")
                f.write("```diff\n")
                f.write(modified_output)
                f.write("\n```\n")
            
            print(f"Diff saved to {output_file}")
            
        except Exception as e:
            print(f"Error comparing {folder_type}/{dir_name}: {str(e)}")
            with open(output_file, 'a') as f:
                f.write(f"비교 중 오류 발생: {str(e)}\n")

def compare_lib_folders(original_lib_path, onchain_lib_path, output_dir="diff_results"):
    """
    두 lib 폴더의 내용을 비교하여 git diff 결과를 마크다운 파일로 저장합니다.
    
    Args:
        original_lib_path: 원본 lib 폴더 경로
        onchain_lib_path: 비교할 onchain lib 폴더 경로
        output_dir: diff 결과를 저장할 디렉토리
    """
    compare_folders(original_lib_path, onchain_lib_path, output_dir, "lib")

def compare_src_folders(original_src_path, onchain_src_path, output_dir="diff_results"):
    """
    두 src 폴더의 내용을 비교하여 git diff 결과를 마크다운 파일로 저장합니다.
    
    Args:
        original_src_path: 원본 src 폴더 경로
        onchain_src_path: 비교할 onchain src 폴더 경로
        output_dir: diff 결과를 저장할 디렉토리
    """
    compare_folders(original_src_path, onchain_src_path, output_dir, "src")

def compare_files_in_directory(original_path, onchain_path, output_file, dir_name, relative_path=""):
    """
    디렉토리 내의 파일 목록을 비교하여 추가/삭제된 파일을 기록합니다.
    
    Args:
        original_path: 원본 디렉토리 경로
        onchain_path: 온체인 디렉토리 경로
        output_file: 결과를 저장할 파일 경로
        dir_name: 디렉토리 이름
        relative_path: 하위 디렉토리를 탐색할 때의 상대 경로
    """
    # 현재 디렉토리의 파일 목록 가져오기
    try:
        original_items = set(os.listdir(os.path.join(original_path, relative_path)))
        onchain_items = set(os.listdir(os.path.join(onchain_path, relative_path)))
    except Exception as e:
        print(f"Error listing directory {relative_path}: {str(e)}")
        return
    
    # 추가/삭제된 파일 목록
    only_original = original_items - onchain_items
    only_onchain = onchain_items - original_items
    common_items = original_items.intersection(onchain_items)
    
    # 결과 기록
    with open(output_file, 'a') as f:
        # 삭제된 파일 목록
        if only_original:
            if not relative_path:
                f.write("### 삭제된 파일 목록\n\n")
                f.write("다음 파일들은 원본에만 존재하고 온체인 버전에서는 삭제되었습니다:\n\n")
            
            for item in sorted(only_original):
                item_path = os.path.join(relative_path, item) if relative_path else item
                original_full_path = os.path.join(original_path, item_path)
                
                if os.path.isdir(original_full_path):
                    f.write(f"- 📁 `{item_path}/` (삭제됨)\n")
                else:
                    f.write(f"- 📄 `{item_path}` (삭제됨)\n")
            
            f.write("\n")
        
        # 추가된 파일 목록
        if only_onchain:
            if not relative_path:
                f.write("### 추가된 파일 목록\n\n")
                f.write("다음 파일들은 온체인 버전에만 존재하고 원본에는 없습니다:\n\n")
            
            for item in sorted(only_onchain):
                item_path = os.path.join(relative_path, item) if relative_path else item
                onchain_full_path = os.path.join(onchain_path, item_path)
                
                if os.path.isdir(onchain_full_path):
                    f.write(f"- 📁 `{item_path}/` (추가됨)\n")
                else:
                    f.write(f"- 📄 `{item_path}` (추가됨)\n")
            
            f.write("\n")
        
        # 공통 파일 목록 (변경 없는 파일 포함)
        if common_items and not relative_path:
            f.write("### 공통 파일 목록\n\n")
            f.write("다음 파일들은 양쪽 버전에 모두 존재합니다:\n\n")
            
            identical_files = []
            modified_files = []
            
            for item in sorted(common_items):
                item_path = os.path.join(relative_path, item) if relative_path else item
                original_full_path = os.path.join(original_path, item_path)
                onchain_full_path = os.path.join(onchain_path, item_path)
                
                # 디렉토리는 별도 표시 (내용 비교 없이)
                if os.path.isdir(original_full_path):
                    f.write(f"- 📁 `{item_path}/`\n")
                    continue
                
                # 파일 내용 비교
                try:
                    diff_cmd = ["git", "diff", "--no-index", "--quiet", original_full_path, onchain_full_path]
                    result = subprocess.run(diff_cmd, capture_output=True, text=True)
                    
                    # 반환 코드 0은 차이가 없음, 1은 차이가 있음을 의미
                    if result.returncode == 0:
                        identical_files.append(item_path)
                        f.write(f"- 📄 `{item_path}` (동일)\n")
                    else:
                        modified_files.append(item_path)
                        f.write(f"- 📄 `{item_path}` (수정됨)\n")
                except Exception as e:
                    print(f"Error comparing files {item_path}: {str(e)}")
                    f.write(f"- 📄 `{item_path}` (비교 실패: {str(e)})\n")
            
            f.write("\n")
            
            # 통계 추가
            f.write("### 파일 비교 통계\n\n")
            f.write(f"- 삭제된 파일: {len(only_original)}개\n")
            f.write(f"- 추가된 파일: {len(only_onchain)}개\n")
            f.write(f"- 수정된 파일: {len(modified_files)}개\n")
            f.write(f"- 동일한 파일: {len(identical_files)}개\n")
            f.write(f"- 총 파일 수: {len(only_original) + len(only_onchain) + len(modified_files) + len(identical_files)}개\n\n")
    
    # 하위 디렉토리 재귀적으로 탐색
    for item in common_items:
        item_path = os.path.join(relative_path, item) if relative_path else item
        original_full_path = os.path.join(original_path, item_path)
        onchain_full_path = os.path.join(onchain_path, item_path)
        
        if os.path.isdir(original_full_path) and os.path.isdir(onchain_full_path):
            compare_files_in_directory(original_path, onchain_path, output_file, dir_name, item_path)

if __name__ == '__main__':
    # 결과 저장 디렉토리
    output_dir = "diff_results"
    
    # 라이브러리 경로 설정
    original_lib_path = "/Users/jonathan/berachain-project/infrared-contracts/lib"
    onchain_lib_path = "/Users/jonathan/berachain-project/infrared_/lib"
    
    # src 폴더 경로 설정
    original_src_path = "/Users/jonathan/berachain-project/infrared-contracts/src"
    onchain_src_path = "/Users/jonathan/berachain-project/infrared_/src"
    
    # lib 폴더 비교 실행
    print("\n===== 라이브러리 폴더 비교 시작 =====")
    compare_lib_folders(original_lib_path, onchain_lib_path, output_dir)
    
    # src 폴더 비교 실행
    print("\n===== 소스 폴더 비교 시작 =====")
    compare_src_folders(original_src_path, onchain_src_path, output_dir) 