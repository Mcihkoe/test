#!/usr/bin/env python3
"""Draft YouTube title / description / tags for a playlist mix.

Usage: python3 tools/make_youtube_meta.py --tracklist output/mix_tracklist.txt --out output/youtube_meta.md
Reads the "M:SS name" tracklist from make_mix.py, gives each track an evocative name,
and checks YouTube limits (title 100, description 5000, tags 500 chars).
"""
import argparse
import random
import re
from pathlib import Path

ADJ = ["Golden", "Lazy", "Sunlit", "Mellow", "Breezy", "Velvet", "Quiet", "Amber", "Easy", "Warm",
       "Slow", "Gentle", "Dreamy", "Soft", "Hazy"]
NOUN = ["Bench", "Fountain", "Picnic", "Promenade", "Lakeside", "Saxophone", "Vinyl", "Iced Coffee",
        "Sunbeam", "Park Lane", "Afternoon", "Elm Walk", "Bandstand", "Daisy", "Skyline"]
TAIL = ["Stroll", "Swing", "Waltz", "Blues", "Serenade", "Groove", "Reverie", "Bossa", "Interlude", "Shuffle"]

TAGS = ["jazz", "jazz music", "relaxing jazz", "cafe jazz", "jazz playlist", "new york jazz",
        "central park", "afternoon jazz", "jazz bgm", "study music", "work music", "background music",
        "chill jazz", "smooth jazz", "lofi jazz", "재즈", "재즈 플레이리스트", "카페 음악", "노동요",
        "공부할때 듣는 음악", "매장음악", "뉴욕 재즈", "1시간 재즈"]


def track_names(n, seed):
    rnd = random.Random(seed)
    names, seen = [], set()
    while len(names) < n:
        style = rnd.random()
        if style < 0.4:
            s = f"{rnd.choice(ADJ)} {rnd.choice(NOUN)}"
        elif style < 0.8:
            s = f"{rnd.choice(NOUN)} {rnd.choice(TAIL)}"
        else:
            s = f"{rnd.choice(ADJ)} {rnd.choice(TAIL)}"
        if s not in seen:
            seen.add(s)
            names.append(s)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracklist", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--hours", default="1")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()

    rows = []
    for line in Path(a.tracklist).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+:\d{2}(?::\d{2})?)\s+(.*)$", line.strip())
        if m:
            rows.append(m.group(1))
    names = track_names(len(rows), a.seed)
    chapters = "\n".join(f"{t} {i:02d}. {nm}" for i, (t, nm) in enumerate(zip(rows, names), 1))

    titles = [
        f"[Playlist] 뉴욕 공원의 오후, 여유로운 재즈 {a.hours}시간 🎷 New York Afternoon Jazz",
        f"햇살 좋은 센트럴파크에서 듣는 카페 재즈 | 공부·작업할 때 듣는 Jazz BGM {a.hours}시간",
        f"New York Afternoon Jazz in the Park 🌿 Relaxing Cafe Jazz for Work & Study ({a.hours} Hour)",
    ]

    desc = f"""🎷 뉴욕 공원의 여유로운 오후, 재즈 한 잔 어떠세요?
햇살 아래 피크닉 매트, 턴테이블에서 흘러나오는 재즈와 함께 {a.hours}시간 동안 쉬어 가세요.
공부, 작업, 독서, 카페 BGM으로 틀어 두기 좋은 플레이리스트입니다.

Relax with a warm afternoon of jazz in a New York park.
Perfect for studying, working, reading, or as cafe background music.

━━━━━━━━━━━━━━━━━━━━
📀 Tracklist
{chapters}
━━━━━━━━━━━━━━━━━━━━

🔔 구독과 좋아요는 다음 플레이리스트 제작에 큰 힘이 됩니다.
🔔 Subscribe for more jazz playlists every week.

ℹ️ 안내 / Notice
- 이 영상의 음악은 자체 제작한 프로그램으로 작곡·합성했으며, 배경 이미지는 AI로 생성했습니다.
- Music composed and synthesized with our own software; background image generated with AI.

#재즈 #재즈플레이리스트 #카페음악 #jazz #relaxingjazz #newyorkjazz
"""

    tags = []
    for t in TAGS:
        if len(",".join(tags + [t])) <= 480:
            tags.append(t)

    checks = [
        ("제목 100자 이하", all(len(t) <= 100 for t in titles), ", ".join(str(len(t)) for t in titles)),
        ("설명 5000자 이하", len(desc) <= 5000, len(desc)),
        ("태그 합계 500자 이하", len(",".join(tags)) <= 500, len(",".join(tags))),
        ("첫 챕터 0:00 시작", rows[:1] == ["0:00"], rows[:1]),
        ("챕터 3개 이상", len(rows) >= 3, len(rows)),
    ]

    md = ["# YouTube 업로드 메타데이터 초안", "", "## 제목 후보 (택 1)", ""]
    md += [f"{i}. {t}" for i, t in enumerate(titles, 1)]
    md += ["", "## 설명란 (그대로 복사)", "", "```", desc.rstrip(), "```", "",
           "## 태그 (쉼표로 구분, 그대로 붙여넣기)", "", "```", ", ".join(tags), "```", "",
           "## 업로드 설정 체크리스트", "",
           "- [ ] 썸네일: `output/thumbnail_ny_afternoon_jazz.jpg` 업로드",
           "- [ ] 변경되거나 합성된 콘텐츠(AI) 공개: **예** (배경 이미지에 사실적인 사람 등장)",
           "- [ ] 카테고리: 음악 / 아동용 아님",
           "- [ ] 재생목록 \"NY Afternoon Jazz\"에 추가",
           "- [ ] 배경 이미지 출처의 상업적 이용 가능 여부 확인",
           "", "## 자동 검사", "", "| 항목 | 결과 | 값 |", "|---|---|---|"]
    md += [f"| {n} | {'OK' if ok else 'FAIL'} | {v} |" for n, ok, v in checks]
    Path(a.out).write_text("\n".join(md) + "\n", encoding="utf-8")
    for n, ok, v in checks:
        print(f"{'OK  ' if ok else 'FAIL'} {n}: {v}")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
