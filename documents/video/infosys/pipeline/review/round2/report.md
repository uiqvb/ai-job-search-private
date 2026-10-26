# Cut check, round 2: Infosys

Length 50.8s, 10 pieces, 9 joins. **1 fail, 18 warning.**

Automatic measurements; the reviewer decides. Pictures: 4 frames around each cut + loudness curve with words.


## Pieces

| # | line | at | len | match | said (re-transcribed) | issues |
|---|---|---|---|---|---|---|
| 0 | 1 Hook | 0.0 | 3.58 | 0.96 | Okay Infosys, at the Australian Open you brought a robot to the Fan Zone. | WARN: words differ at the end: raw '' vs cut 'zone' |
| 1 | 2 Open Day | 3.58 | 2.21 | 0.8 | I too brought mine to the Deakin Open Day. | WARN: words differ at the start: raw '' vs cut 'i'; WARN: words differ at the end: raw '' vs cut 'open day' |
| 2 | 3 Meet | 5.79 | 8.56 | 0.96 | It started as two separate uni projects, an API and a robot. Nobody said that they should  | WARN: words differ at the start: raw '' vs cut 'it'; WARN: words differ at the end: raw '' vs cut 'meet' |
| 3 | 4 Chair | 14.35 | 5.02 | 0.97 | My unit chef warned me that I might finish neither and for a month he was right. | WARN: words differ at the start: raw '' vs cut 'my' |
| 4 | 5 Worked | 19.37 | 4.6 | 1.0 | Then it worked. 100 out of 100 and it got picked for Deakin's Open Day. |  |
| 5 | 6 MatchFeel | 23.97 | 5.66 | 0.88 | That's why MatchFeel got me. No one expects to follow tennis by touch. You built it anyway | WARN: words differ at the start: raw '' vs cut 'that's'; WARN: words differ at the end: raw '' vs cut 'anyways' |
| 6 | 7 Robot | 29.63 | 4.43 | 0.88 | Same with my robot. Nobody asked me to build it but I still built it anyway. | WARN: words differ at the end: raw '' vs cut 'anyway' |
| 7 | 8 InStep | 34.06 | 3.75 | 0.56 | That's the work I want at InStep. AI and robots that leave the screen. | WARN: words differ at the start: raw 'wanted in step' vs cut 'that's the work i want at instep'; WARN: re-transcription only matches 56% of the raw words (check for garbled audio) |
| 8 | 9 ML gap | 37.81 | 4.98 | 0.6 | I haven't created an ML model yet but that's what I want to learn from InStep and its ment | WARN: words differ at the start: raw '' vs cut 'i haven't created an ml model yet but'; WARN: words differ at the end: raw '' vs cut 'mentors'; WARN: re-transcription only matches 60% of the raw words (check for garbled audio) |
| 9 | 10 Close | 42.79 | 7.96 | 0.98 | So yeah, I'm Manit Khera and I usually end up doing more than what is asked of me. Thank y | WARN: words differ at the start: raw '' vs cut 'so' |

## Joins

| # | at | between | gap | loud jump | issues | picture |
|---|---|---|---|---|---|---|
| 1 | 3.58 | 1 Hook -> 2 Open Day | 0.33 | 2.0 | ok | pipeline/review/round2/join_01.png |
| 2 | 5.79 | 2 Open Day -> 3 Meet | 0.26 | 0.9 | ok | pipeline/review/round2/join_02.png |
| 3 | 14.35 | 3 Meet -> 4 Chair | 0.23 | None | ok | pipeline/review/round2/join_03.png |
| 4 | 19.37 | 4 Chair -> 5 Worked | 1.19 | 2.0 | FAIL: dead air 1.19s | pipeline/review/round2/join_04.png |
| 5 | 23.97 | 5 Worked -> 6 MatchFeel | 0.26 | 5.4 | WARN: loudness changes 5.4 dB | pipeline/review/round2/join_05.png |
| 6 | 29.63 | 6 MatchFeel -> 7 Robot | 0.26 | 4.8 | WARN: loudness changes 4.8 dB | pipeline/review/round2/join_06.png |
| 7 | 34.06 | 7 Robot -> 8 InStep | 0.29 | 3.6 | ok | pipeline/review/round2/join_07.png |
| 8 | 37.81 | 8 InStep -> 9 ML gap | 0.26 | 1.2 | ok | pipeline/review/round2/join_08.png |
| 9 | 42.79 | 9 ML gap -> 10 Close | 0.35 | 6.6 | WARN: loudness changes 6.6 dB | pipeline/review/round2/join_09.png |

Start and end: pipeline/review/round2/start_end.png
