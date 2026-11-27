from pathlib import Path
import pandas as pd

################
################
def 정제(df):
	result = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	result = result.dropna(subset=["점수"])
	print(f"점수 결측 행 삭제 후: {len(result)}행")

	# 모든 열이 같은 중복 행을 삭제한다.
	result = result.drop_duplicates()
	print(f"중복 행 삭제 후: {len(result)}행")

	# 반과 과목의 앞뒤 공백을 제거한다.
	result["반"] = result["반"].str.strip()
	result["과목"] = result["과목"].str.strip()
	print(f"공백 제거 후: {len(result)}행")

	# 점수가 0~100 범위를 벗어난 행을 삭제한다.
	result = result[result["점수"].between(0, 100)]
	print(f"유효 점수 필터링 후: {len(result)}행")

	return result

import pandas as pd
df = pd.read_csv(Path(__file__).with_name("scores_2026.csv"))
df = 정제(df)
print(sorted(df["반"].unique())) # ['1반', '2반']       ← 세 개에서 두 개로
print(sorted(df["과목"].unique())) # ['수학','영어','프로그래밍'] ← 네 개에서 세 개로
cleaned_df = df.copy()

# 시작        114
# 빈 칸 제거  108      ← 114 - 108 = 6    진단표의 「빈 칸」과 같은가?
# 중복 제거   104      ← 108 - 104 = 4    진단표의 「중복」과 같은가?
# 범위 밖 제거 100     ← 104 - 100 = 4    999 세 개 + 음수 하나


csv_path = Path(__file__).with_name("scores_2026.csv")
df = pd.read_csv(csv_path)
print(df.shape) # (114, 5)
print(df["점수"].isna().sum()) # 6      ← 빈 칸이 몇 개인가
print(df.duplicated().sum()) # 4      ← 완전히 같은 행이 몇 개인가
print(df["반"].unique()) # ['2반' '1반' '1반 ']      ← 세 개?
print(df["과목"].unique()) # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(df["점수"].describe()) # max 999.0  min -5.0   ← 점수인데?

# 정제된 데이터에서 수학 과목만 남긴다.
df = cleaned_df[cleaned_df["과목"] == "수학"]
print(f"수학 행 수: {len(df)}행")

# 정제된 데이터를 반별로 묶어 점수 평균을 계산한다.
반별_평균 = cleaned_df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

# 정제된 데이터를 과목과 반별로 묶어 점수 평균을 계산한다.
과목_반별_평균 = cleaned_df.groupby(["과목", "반"])["점수"].mean()
print("과목별, 반별 점수 평균:")
print(과목_반별_평균)

# 반별 점수 개수, 평균, 중앙값, 최댓값을 한 표로 계산한다.
반별_통계표 = cleaned_df.groupby("반")["점수"].agg(
	["count", "mean", "median", "max"]
).round(2)
반별_통계표 = 반별_통계표.rename(
	columns={"count": "개수", "mean": "평균", "median": "중앙값", "max": "최댓값"}
)
print("반별 점수 통계:")
print(반별_통계표.to_string(float_format=lambda 값: f"{값:.2f}"))

