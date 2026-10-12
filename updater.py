import json
import os
import sys

def run_updater(input_path="ritual-history-2026-10-12.json", output_html="index.html"):
    if not os.path.exists(input_path):
        print(f"[Error] 입력 파일 '{input_path}'를 찾을 수 없습니다.")
        return False

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_days = len(days)

    # 1. 확정적 통계 계산 (두 번 돌려도 동일)
    open_count = sum(1 for d in days if d.get("open") is not None)
    close_count = sum(1 for d in days if d.get("close") is not None)
    
    # 강점 실천율 계산
    practiced_count = sum(
        1 for d in days 
        if d.get("close") and any("실천했다" in item for item in d.get("close", []))
    )
    practice_rate = round((practiced_count / total_days) * 100, 1) if total_days > 0 else 0

    print("=== [새로 쓰는 장치 분석 결과] ===")
    print(f"* 분석 대상: {data.get('student', '김민승')}")
    print(f"* 전체 기록 일수: {total_days}일")
    print(f"* 아침 리추얼 작성: {open_count}회")
    print(f"* 저녁 성찰 작성: {close_count}회")
    print(f"* 강점 행동 실천율: {practice_rate}% ({practiced_count}/{total_days}일)")

    # 2. 날짜와 근거가 붙은 역량 문단 후보 생성
    latest_day = days[-1] if days else {}
    latest_date = latest_day.get("date", "2026-10-12")
    
    candidate_paragraph = (
        f"<!-- AUTO-GENERATED: {latest_date} -->\n"
        f"<p><span class=\"tag\">[지속력 근거: {latest_date}]</span> "
        f"총 {total_days}일간의 리추얼 중 {open_count}회의 아침 몰입과 {close_count}회의 성찰을 완수했습니다. "
        f"강점 실천율 {practice_rate}%를 유지하며, 통제할 수 없는 일에 조급해하지 않고 "
        f"주어진 네트워크 과업에 묵묵히 전념하는 엔지니어의 일관된 태도를 증명하고 있습니다.</p>"
    )

    print("\n=== [생성된 문단 후보] ===")
    print(candidate_paragraph)

    # 3. index.html 파일 내 숫자 갱신 (선택적)
    if os.path.exists(output_html):
        with open(output_html, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 25일 연속 -> total_days일 연속으로 갱신
        updated_content = content.replace("25일 연속", f"{total_days}일 연속")
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"\n* '{output_html}' 파일의 리추얼 숫자가 '{total_days}일 연속'으로 안전하게 갱신되었습니다.")

    return True

if __name__ == "__main__":
    run_updater()
