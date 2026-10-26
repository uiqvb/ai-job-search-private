# Cut check, round 1: Infosys

Length 53.8s, 11 pieces, 10 joins. **3 fail, 20 warning.**

Automatic measurements; the reviewer decides. Pictures: 4 frames around each cut + loudness curve with words.

- **WARN** line '9 ML gap' is used 2 times

## Pieces

| # | line | at | len | match | said (re-transcribed) | issues |
|---|---|---|---|---|---|---|
| 0 | 1 Hook | 0.0 | 4.05 | 1.0 | Okay Infosys, at the Australian Open you brought a robot to the Fan Zone. |  |
| 1 | 2 Open Day | 4.05 | 2.43 | 0.88 | I too brought mine to the Deakin Open Day. | WARN: words differ at the end: raw '' vs cut 'open day' |
| 2 | 3 Meet | 6.48 | 8.56 | 0.96 | It started as two separate uni projects, an API and a robot. Nobody said that they should  | WARN: words differ at the start: raw '' vs cut 'it'; WARN: words differ at the end: raw '' vs cut 'meet' |
| 3 | 4 Chair | 15.04 | 5.02 | 0.97 | My unit chef warned me that I might finish neither and for a month he was right. | WARN: words differ at the start: raw '' vs cut 'my' |
| 4 | 5 Worked | 20.06 | 4.6 | 1.0 | Then it worked. 100 out of 100 and it got picked for Deakin's Open Day. |  |
| 5 | 6 MatchFeel | 24.66 | 5.66 | 0.88 | That's why MatchFeel got me. No one expects to follow tennis by touch. You built it anyway | WARN: words differ at the start: raw '' vs cut 'that's'; WARN: words differ at the end: raw '' vs cut 'anyways' |
| 6 | 7 Robot | 30.32 | 4.43 | 0.88 | Same with my robot, nobody asked me to build it. But I still built it anyway. | WARN: words differ at the end: raw '' vs cut 'anyway' |
| 7 | 8 InStep | 34.75 | 3.75 | 0.56 | That's the work I want at InStep. AI and robots that leave the screen. | WARN: words differ at the start: raw 'wanted in step' vs cut 'that's the work i want at instep'; WARN: re-transcription only matches 56% of the raw words (check for garbled audio) |
| 8 | 9 ML gap | 38.5 | 2.41 | 0.77 | I haven't trained a machine model yet. | WARN: words differ at the start: raw '' vs cut 'i'; WARN: words differ at the end: raw '' vs cut 'yet'; WARN: re-transcription only matches 77% of the raw words (check for garbled audio) |
| 9 | 9 ML gap | 40.91 | 4.88 | 0.6 | I haven't trained an ML model yet, but that's what I want to learn from InStep and its men | WARN: words differ at the start: raw '' vs cut 'i haven't trained an ml model yet but'; WARN: words differ at the end: raw '' vs cut 'mentors'; WARN: re-transcription only matches 60% of the raw words (check for garbled audio) |
| 10 | 10 Close | 45.79 | 7.96 | 0.98 | So yeah, I'm Manit Khera and I usually end up doing more than what is asked of me. Thank y | WARN: words differ at the start: raw '' vs cut 'so' |

## Joins

| # | at | between | gap | loud jump | issues | picture |
|---|---|---|---|---|---|---|
| 1 | 4.05 | 1 Hook -> 2 Open Day | 0.91 | 1.2 | FAIL: dead air 0.91s | pipeline/review/round1/join_01.png |
| 2 | 6.48 | 2 Open Day -> 3 Meet | 0.24 | 0.3 | ok | pipeline/review/round1/join_02.png |
| 3 | 15.04 | 3 Meet -> 4 Chair | 0.21 | None | ok | pipeline/review/round1/join_03.png |
| 4 | 20.06 | 4 Chair -> 5 Worked | 1.2 | 1.6 | FAIL: dead air 1.20s | pipeline/review/round1/join_04.png |
| 5 | 24.66 | 5 Worked -> 6 MatchFeel | 0.26 | 5.1 | WARN: loudness changes 5.1 dB | pipeline/review/round1/join_05.png |
| 6 | 30.32 | 6 MatchFeel -> 7 Robot | 0.25 | 5.0 | WARN: loudness changes 5.0 dB | pipeline/review/round1/join_06.png |
| 7 | 34.75 | 7 Robot -> 8 InStep | 0.29 | 3.8 | ok | pipeline/review/round1/join_07.png |
| 8 | 38.5 | 8 InStep -> 9 ML gap | 0.25 | 1.0 | ok | pipeline/review/round1/join_08.png |
| 9 | 40.91 | 9 ML gap -> 9 ML gap | 0.26 | 0.7 | FAIL: words repeated across the cut: 'i haven't trained' | pipeline/review/round1/join_09.png |
| 10 | 45.79 | 9 ML gap -> 10 Close | 0.25 | 6.5 | WARN: loudness changes 6.5 dB | pipeline/review/round1/join_10.png |

Start and end: pipeline/review/round1/start_end.png
