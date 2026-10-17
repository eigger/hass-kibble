# 공통 규칙 적용 체크리스트

hass-kibble 최초 채택 파일럿의 실제 확인 기록입니다. [사용법과 판정 기준](https://github.com/eigger/hass-repo-standards/blob/103124f47c6fc838a39eddbd008e64cfb1a5e5f0/docs/checklist.md)을 읽고, 아래 규칙은 `STANDARDS.md`에 기록한 표준 커밋에서 확인합니다. 태그·릴리스 대신 검토한 표준 커밋 SHA를 기준으로 합니다.

## 검토 대상

| 항목 | 값 |
|---|---|
| 통합 리포 / 실제 기본 브랜치 | eigger/hass-kibble / master |
| domain / 구현 경로 | kibble / custom_components/kibble/ |
| 검토 대상 통합 커밋 / 채택 PR | f1a70396bea833b25e8fbcac7fa837ac3769ec91 — 지원 최소 복원 완료; [PR #8](https://github.com/eigger/hass-kibble/pull/8)의 e01 이력과 구분, 문서 마감은 후속 별도 커밋 |
| 검토한 표준 전체 커밋 SHA | 103124f47c6fc838a39eddbd008e64cfb1a5e5f0 |
| 검토일 / 조율 담당 | 2026-10-17 / root |
| 구현 서브 에이전트 / 독립 리뷰·검증 서브 에이전트 | implement_kibble_pilot / review_kibble_pilot |
| 중앙 현황표 반영일 / 기록 | 2026-10-17 — 중앙 4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28에 실제 구현·검증 종료 보고 등록; 표 상태 완료 전환은 문서 마감 후 별도 반영 |
| profile / 테스트 경로 | integration / ha, tests/components/kibble/ |
| 이전 검토 기록 | 최초 채택 |
| 채택 판정 | 완료 — 적용 대상 필수 PASS/N/A, 현재 예외 없음. 중앙 종료 보고 등록 완료; 표 상태 전환은 문서 마감 후 후속 반영 |

상태: `TODO` = 미확인·미충족, `PASS` = 근거로 확인, `EXCEPTION` = 적용 대상의 기록된 예외, `N/A` = 적용 조건에 해당 없음. 이 기록은 실제 확인 근거로 판정했습니다. 권장 항목과 수동 검증 한계는 별도로 적었습니다.

## 채택·구조·사용자 데이터

| 규칙 ID | 확인 항목 | 상태 | 근거 / 남은 작업 |
|---|---|---|---|
| GOV-01, GOV-02 | `STANDARDS.md`에 표준 SHA·profile·실제 기본 브랜치·예외 기록, workflow/action은 검토 SHA로 고정 | PASS | STANDARDS.md와 workflow를 중앙 파일럿 보완 커밋 103124f47c6fc838a39eddbd008e64cfb1a5e5f0으로 고정 |
| GOV-03 | 새 표준 채택 변경의 영향·이관 방법과 명시적 채택 PR 확인. 규칙 자체를 변경하면 공통 CHANGELOG 기록 | PASS | 최종 채택 PR #8 독립 검증·CI 후 squash merge e01ac2119c4ce571ffe82ab2b189173fc6c78b88; 초기 직접 반영 예외는 STANDARDS에 이력 보존 후 해제 |
| GOV-04 | 중앙 표에 작업 시작·단계 변경·종료 상태, 담당·적용 내용·검증/리뷰 근거·남은 작업 갱신, 타 리포 기록 보존 | PASS | 중앙 4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28에 실제 f1a 구현·검증 종료 결과 등록 완료. 표 상태 전환만 문서 마감 후 별도 반영 |
| GOV-05 | 구현과 독립 리뷰·검증을 별도 서브 에이전트에게 위임, 지적 수정·재검증 및 결과 취합 | PASS | 구현 implement_kibble_pilot / 독립 review_kibble_pilot 분리; 초기 파일럿 독립 양환경 30 passed·pip check·정책 검토 완료; PR #8 당시 지원 변경 검증과 분리해 현재 지원 하한 복원 작업의 최신·최소 환경 각각 독립 31 passed·pip check·Ruff·format 통과 |
| HA-01, HA-13 | `custom_components/<domain>/`와 domain 일치, 필요한 모듈·공개 API·생명주기는 Core 대응 구조 | PASS | 기존 Core 대응 api/config_flow/coordinator/sensor/button/runtime_data 구조 유지 |
| HA-02 | manifest 필드·정렬·동작 선언 확인, 공식 품질 등급 자가 표기 없음 | PASS | manifest: kibble, local_polling, config_flow, requirements=[], version0.1.5; 알파벳순·자가등급 없음 |
| HA-03 (권장) | 공통 상수·설정·갱신·플랫폼 역할 및 프로토콜 경계에 맞게 모듈 구성 | PASS | const/config_flow/coordinator/api와 플랫폼 역할 분리 유지 |
| HA-04, HA-08 | UI 설정·중복·안정적 식별 및 기능별 options/reauth/reconfigure, entity 의미·registry 영향 확인 | PASS | test_config_flow: 생성·중복·실패·재인증; test_sensor registry unique ID/단위/상태 |
| HA-01, HA-04, HA-08, REL-01, REL-03 | domain·unique ID·entry schema·상태/통계 계약 변경 시 migration 테스트와 사용자 조치 안내 | N/A | domain·ID·entry schema·상태/통계 계약 변경 없음; migration 대상 없음 |
| HA-05, HA-06 | setup 실패 구분, unload/reload·부분 실패의 task/listener/연결 정리, async·timeout·취소 처리 | PASS | test_init 실제 manager setup/reload/unload, listener·refresh timer 정리와 setup retry/auth 구분; async aiohttp+15초 timeout |
| HA-07 | 중복 polling·property I/O 방지, push 보존, unavailable/unknown·실패 후 복구 | PASS | 단일 coordinator polling; test_coordinator 실패 시 last-good 유지·오류수·복구(기존 명시 계약), test_sensor weight unknown |
| HA-11, HA-12 | 번역·action/schema 일치, 로그/diagnostics/fixture 비식별화와 제공 시 redaction 테스트 | PASS | 기존 en/ko 번역 유지; API 오류에 network exception 원문 제거·비밀정보 회귀, 반복 실패 첫 WARNING 후 DEBUG; diagnostics 미제공 |

## 실제 HA 테스트·호환성·의존성

| 규칙 ID | 확인 항목 | 상태 | 근거 / 남은 작업 |
|---|---|---|---|
| TEST-08 | `tests/components/<domain>/`에 구현과 대응하는 테스트·domain fixture 배치, discovery·CI 경로 일치 | PASS | tests/components/kibble/ + fixtures/state.json; pytest testpaths·CI 경로 동일 |
| TEST-02, TEST-03, DEP-07 | 실제 HA·호환 플러그인과 `hass`/`enable_custom_integrations` fixture 사용, HA core stub/복사본/`--no-deps`로 대체하지 않음 | PASS | 실제 hass/enable_custom_integrations/MockConfigEntry; sys.modules stub 제거; current HA2026.10.2/plugin0.13.373와 minimum HA2025.3.0/plugin0.13.221 별도 실제 환경 |
| TEST-09 | 실제 loader·config entry manager로 setup/플랫폼 로딩, HA 상태·registry·service/action으로 결과 검증 | PASS | test_init/test_sensor/test_button/test_config_flow 실제 loader·entry·state·registry·서비스·flow manager |
| TEST-01, TEST-06, TEST-07 | 구현 기능별 성공·실패·중복·migration·unload·복구 회귀 검증, 외부 통신 경계만 mock, skip 사유 | PASS | 기존API17개+센서6/coord3의 회귀의미 보존·확장; HTTP 경계 mock, reload/unload/flow/버튼 추가; 현재·최소 HA 두 환경 및 정확한 환경 설치값·지원 하한 검사, 아래 검증 결과 |
| TEST-04, HACS-01 | 선언한 최소 HA의 정확한 버전과 호환 Python/플러그인으로 실제 HA 테스트 | PASS | hacs.json 최소 HA2025.3.0 복원·유지, minimum HA2025.3.0/plugin0.13.221/Python3.13 별도 검증 |
| TEST-05, HA-10, DEP-02, DEP-05 | imagespec·blesession 등 최소/현재 라이브러리 별도 환경, 실제 HA 테스트·정확한 설치값·API 경계 검증 | N/A | manifest runtime requirements=[]; imagespec/blesession 등 하한검사 없음 |
| DEP-01, DEP-06 | Python runtime은 manifest requirements, HA domain은 dependencies/after_dependencies, 테스트·린트 requirements는 별도 | PASS | runtime requirements=[] 유지; HA/plugin/Ruff 테스트파일 분리; button/sensor HA 플랫폼 설치 입력 |
| DEP-07, CI-06 | 실제 사용하는 HA 구성요소의 requirements·필수 재귀 의존성·선택 로딩 경로 설치, resolver·`pip check` 통과 | PASS | 현재·최소 HA resolver·pip check 정상; 사용 button/sensor manifest 외부 requirements 없음 |
| DEP-02, DEP-03, DEP-08 | 의존성 추가/변경의 버전·extras·marker·선언 위치·지원 플랫폼·라이선스 검토, 실제 HA 테스트와 문서 갱신 | PASS | 테스트 전용 exact HA/plugin/Ruff; 과거 최소 환경·공식helper constraints 복원·별도 격리; runtime 추가 없음 |

최신 테스트 HA와 컴포넌트 지원 최소 HA는 별개입니다. 각 실제 실행 환경·대상 커밋·CI를 따로 기록하고, 지원 하한 검증을 최신 환경의 성공으로 대신하지 않습니다.

| 검증 축 / 상태 | 통합 커밋 | Python / HA / 플러그인 실제 버전 | 대상 패키지 실제 버전·extras·marker | 명령·테스트 결과·pip check / CI run·job | skip·제외·미검증 범위 |
|---|---|---|---|---|---|
| 현재 테스트 HA / PASS | f1a70396bea833b25e8fbcac7fa837ac3769ec91 | 로컬 Python3.14.5·GitHub Ubuntu Python3.14.8 / HA2026.10.2 / plugin0.13.373 | runtime package 없음 | 구현·독립 및 master Tests39034355878 각각 31 passed·pip check·Ruff·format PASS | 실서버·HA frontend UI 미검증 |
| 정확한 최소 지원 HA / PASS | 동일 | 로컬 Python3.13.14·GitHub Ubuntu Python3.13.16 / HA2025.3.0 / plugin0.13.221 | aiohttp3.11.13 + 공식helper constraints | 구현·독립 및 master Tests39034355878 각각 31 passed·pip check·Ruff·format PASS | 실서버·HA frontend UI 미검증 |
| 정확한 최소 라이브러리 / N/A | 동일 | 동일 | manifest requirements=[] | 대상 없음 | 해당 없음 |

## HACS·CI·의존성 업데이트

| 규칙 ID | 확인 항목 | 상태 | 근거 / 남은 작업 |
|---|---|---|---|
| HACS-01, HACS-02 | 루트 README/LICENSE/hacs.json, 검증한 최소 HA, 실제 배포 구조와 필요한 옵션 일치 | PASS | README/LICENSE/hacs.json 및 custom_components/kibble 배포 구조 유지; 정확최소 검증 |
| HACS-03, HACS-05 | Default 여부는 목록 근거로 확인, HACS/Hassfest 실제 실행, ignore는 이유·해제 조건 기록 | PASS | Custom 배지·MIT 로컬 브랜드 icon256/2x512·출처/재현방법 제공; master f1a70396bea833b25e8fbcac7fa837ac3769ec91 Validate39034355875 HACS 9/9·Hassfest 성공, ignore 없음 |
| HACS-06 (권장) | description·topics·issue 경로·brands 및 사용하는 HACS 필드 지원 확인 | PASS | description/topics/issues/hacs.json 실제 HACS PASS; 로컬 MIT 브랜드 파일·PNG 시각검사·독립 재생성검증 및 master Validate 성공. HA frontend UI 실표시는 미검증 |
| CI-01, CI-02 | Validate/Python Tests 공통화, 확장 job 유지, PR·실제 기본 브랜치 push·dispatch 및 필요한 schedule | PASS | 공통 Python Tests 최신·최소 HA 두 job·Validate 호출; PR/master push/dispatch/주간schedule |
| CI-03, CI-05, CI-08 | 최소 권한·checkout 자격증명 비보존·timeout·concurrency, full SHA·갱신 관리, 비신뢰 입력·secrets 경계 | PASS | caller contents:read, workflow+ref concurrency, fullSHA, 중앙 timeout/credential비보존, Dependabot Actions갱신 |
| CI-04, CI-07, CI-12 | 실패를 숨기지 않는 실제 `ha` 필수 테스트, 버전별 환경·cache·Ruff 설정과 required checks 이름 확인 | PASS | 실제 최신·최소 HA 두 환경 복원; master f1a70396bea833b25e8fbcac7fa837ac3769ec91 Tests39034355878에서 각31 passed·pip check/Ruff/format 성공, required checks 설정 변경 없음 |
| DEP-03, DEP-04, CI-09 | updater의 선택 package·연산자/extras/marker 보존, 안정 버전·major 정책, 실제 기본 브랜치·단일 bot branch·PR만 제안 | N/A | runtime requirements=[]; manifest updater 대상 없음; Dependabot은 테스트/Actions PR만 제안 |
| CI-09, CI-10, DEP-08 | 변경 tree의 새 하한·실제 HA 검증 후 PR 동기화, 실패 시 중단·변경 없음 시 기존 PR 정리, 후속 required checks 충족 방식 확인 | N/A | manifest updater 없음; GITHUB_TOKEN update PR 후속검사 운영 대상 없음 |

## README·Bluetooth·유지보수

| 규칙 ID | 확인 항목 | 상태 | 근거 / 남은 작업 |
|---|---|---|---|
| DOC-01, DOC-02, DOC-06 | README 구성·기존 언어·번역 연결, 요구사항/설정 예시·개발/실HA 테스트/의존성 안내와 검증 범위 | PASS | 한국어 main/영어 번역 보존·전환링크; 요구/설치/엔티티/사용/제한/개발/지원 문서 |
| DOC-03, DOC-04, DOC-05 | 제목 아래 관리 블록, flat-square·순서·실제 조건별 배지, CI 실제 기본 브랜치, opt-in Usage 의미·이전 안내 보존 | PASS | .hass-standards.json 두 README 관리블록; HACS/실제0.1.5Release/최소HA/Tests/Validate/License 순서·master·flat-square; Usage 비활성 |
| HA-09, HA-10 | BLE 사용 시 HA Bluetooth API·라이브러리 공개 경계, 지원한 proxy 경로·재연결·취소·서비스 변경 검증 | N/A | HTTP local_polling 통합; Bluetooth/imagespec/blesession 없음 |
| DOC-07 | blesession/proxy 통합 README에서 공통 Bluetooth 설정·추천 기기/리비전·active 연결/스캔 차이·문제 해결 안내로 연결 | N/A | Bluetooth proxy 사용 없음 |
| DOC-07, HA-12 | 기기별 깨우기·인증·타 앱 연결·전송 제약, 실제 검증 경로와 미검증 범위, 공개 문제 로그 비식별화 | PASS | Bluetooth 기기조건 N/A; README 문제보고 토큰/개인URL/반려동물정보 제거 및 실서버 미검증 명시 |
| REL-01, REL-03 | 테스트 최신화와 지원 하한 분리 및 기존 지원 유지 안내 | PASS | PR #8의 일시적 지원 상향을 정정해 기존 최소2025.3.0 복원; README 최신 테스트2026.10.2와 분리, domain·ID·entry schema 변경 없음 |
| HACS-04, REL-02, CI-11 | 실제 릴리스의 동일 검증 commit/tag·manifest·산출물·권한 | N/A | 이번 작업에서는 release/tag/manifest.version 변경 없음; 다음 릴리스 시 별도 확인 |
| REL-04 | 이전/중단 시 README 상단 경로·유지보수 상태·재등록 여부, 자동 이전으로 오인하지 않는 안내 | N/A | 이전/중단 작업 없음 |
| REL-05 (권장) | 의존성/HA API 변경과 기능 변경 분리, 표준 변경은 명시적 채택 PR로 반영 | PASS | 기능/domain/ID/통계계약 유지, 테스트/CI/문서 공통화 및 오류정보 보호·중복경고만 보완 |

## 예외와 남은 작업

예외 원본은 `STANDARDS.md`입니다. 최종 PR #8 검토로 기존 GOV-03 예외를 해제했으며, 현재 예외는 없습니다. 최초 직접 반영 이력은 STANDARDS에 보존했습니다.

| 규칙 ID | 예외 위치 / 이유 | 담당자 | 재검토 조건 |
|---|---|---|---|
| 없음 | [STANDARDS.md](STANDARDS.md#예외)에서 초기 예외 해제 근거와 이력 확인 | root / reviewer | 새 예외 발생 시 기록 |

| 구분 | 후속 조치·검증 한계 | 담당자 | 근거 |
|---|---|---|---|
| 행정 후속 | 중앙 표 상태를 완료로 전환하고 문서 마감 커밋 기록 | root | 종료 결과는 이미 중앙 4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28에 등록 |
| 수동 검증 한계 | 실물·운영 Kibble 서버 및 HA frontend UI 미검증 | 유지보수 담당 | HTTP 경계 대체 실제 HA 테스트·PNG 시각 검사·HACS 검증과 구분 |

현재 적용 대상 필수 TODO와 EXCEPTION은 없습니다. 기능이 없는 N/A와 실물·UI 수동 검증 한계는 필수 자동 테스트 성공과 구분했습니다. CI 성공만으로 실물 기기 검증을 주장하지 않습니다.

중앙 보고는 [종료 보고 등록 커밋](https://github.com/eigger/hass-repo-standards/blob/4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28/docs/adoption-status.md)에 반영했습니다. 기준 규칙 SHA는 `103124f47c6fc838a39eddbd008e64cfb1a5e5f0`로 유지하며 현황 기록 커밋과 혼동하지 않습니다.

## 초기 파일럿 독립 리뷰·검증 기록 (이전 지원 정책)

2026-10-17 `/root/review_kibble_pilot`이 구현과 분리한 pip 환경에서 중앙 installer를 통해 현재·최소 HA를 각각 설치하고 30개 테스트와 pip check 성공을 확인했습니다. 최소 환경은 `constraints/homeassistant-min.txt`를 포함해 재검증했습니다. 변경 코드·65개 규칙·체크리스트·실제 명령과 결과를 검토했고 미해결 필수 지적이 없었습니다. 이 과거 환경의 실행 결과는 이력이며 현재 지원 버전은 최신 정책과 아래 최종 검증 기록을 따릅니다.

## 최초 원격 검증과 보완

통합 커밋 `29e07c469a9c14e42f645cf24ccf0f1ace25c202`의 [Tests 39032907613](https://github.com/eigger/hass-kibble/actions/runs/39032907613)은 현재·최소 HA 각각 30 passed와 pip check, Ruff·format을 통과했습니다. [Validate 39032907660](https://github.com/eigger/hass-kibble/actions/runs/39032907660)은 Hassfest 성공, HACS 8/9 검사 성공, brands 검사 실패였습니다. 로컬 브랜드 아이콘 미제공 및 HA brands 미등록이 원인입니다. 기존 Kibble MIT 512px 자산을 icon@2x.png로 보존하고 HA 규격의 256px icon.png를 재현 가능한 변환으로 제공해 이후 Validate에서 해결을 확인했습니다.

## 자산 규격 보완 검증 이력 (이전 지원 정책)

중간 커밋 `6d83784305d37739046938b40b660098ffad3332`의 [Tests 39033147568](https://github.com/eigger/hass-kibble/actions/runs/39033147568)와 [Validate 39033147587](https://github.com/eigger/hass-kibble/actions/runs/39033147587)은 모두 성공했습니다. 이후 HA 이미지 규격에 맞춰 원본을 512px `icon@2x.png`로 보존하고 재현 가능한 256px `icon.png`를 제공했습니다. 이 자산 보완 커밋 `fb57b75868af5db5d45d1a7f6b42c7f496564cbe`의 [Tests 39033254106](https://github.com/eigger/hass-kibble/actions/runs/39033254106)와 [Validate 39033254177](https://github.com/eigger/hass-kibble/actions/runs/39033254177)의 결과는 해당 run에서 확인합니다. 이후 PR #8에서 지원 정책을 일시 변경했으므로 그 이력을 현재 지원 검증으로 대신하지 않습니다.

## PR #8 당시 지원 정책 변경 이력 (정정 전)

PR #8에서는 최신 테스트 갱신과 지원 하한을 혼동해 최소 지원 HA를 2026.10.2로 상향했습니다. 이 상태는 아래 정정 커밋에서 기존 지원 하한으로 되돌렸습니다. 현재 PyPI의 호환 최신 조합은 HA2026.10.2와 플러그인0.13.373이며 Python3.14.2 이상이 필요합니다. 구 최소 HA workflow job·requirements·Bluetooth helper constraints를 제거했습니다. 기존 Dependabot PR #8의 downgrade와 구 최소 환경 동시 변경은 이 정책에 맞게 정정하고, 삭제된 환경만 변경하는 #9~12는 이관 완료로 오인하지 않고 불필요 PR로 정리합니다. 최신 정책의 별도 독립 검증과 PR #8 및 master CI 성공 결과는 아래 기록에 연결했습니다.

2026-10-17 최신 지원 정책 변경을 `/root/review_kibble_pilot`이 독립 pip 환경에서 재검증했습니다. HA2026.10.2/플러그인0.13.373/Python3.14.5에서 실제 HA 테스트 31 passed, pip check·Ruff·format 성공, 최소지원과 requirements/설치 HA 동기화 검사도 통과했습니다. 해당 PR에서 사용했던 당시 중앙 기준은 `a6deb61613407c099b28cbbe826ba89be1464e7d`이며 현재 지원 하한 복원 작업의 기준과 다릅니다. PR #8 head와 squash merge 결과는 아래 최종 검증 기록에서 확인합니다.

## 이전 PR #8과 master 검증 이력

[PR #8](https://github.com/eigger/hass-kibble/pull/8)은 head `763fdbad101c2021bc95a7ea34da84b84e0a465d`에서 [Tests 39033651073](https://github.com/eigger/hass-kibble/actions/runs/39033651073)와 [Validate 39033651170](https://github.com/eigger/hass-kibble/actions/runs/39033651170) 성공을 확인한 뒤 squash merge했습니다. 실제 HA 테스트 31 passed, pip check·Ruff·format 및 HACS·Hassfest를 통과했습니다. 검증 대상 구현 커밋은 master `e01ac2119c4ce571ffe82ab2b189173fc6c78b88`입니다. master의 [Tests 39033920073](https://github.com/eigger/hass-kibble/actions/runs/39033920073)와 [Validate 39033920133](https://github.com/eigger/hass-kibble/actions/runs/39033920133)은 모두 성공했으며, 독립 리뷰 담당이 실제 run 결과와 테스트 로그를 확인했습니다.

PR #9~12는 삭제한 과거 최소 환경만 변경하는 제안이므로 root가 폐기 사유를 남기고 닫았습니다. 해당 변경을 병합하거나 검증 완료한 것으로 기록하지 않습니다. 이 문서 마감은 구현 검증을 기록하는 후속 별도 변경이며, 자기 커밋의 사전 검증을 뜻하지 않습니다. 실물·운영 서버 및 HA frontend UI는 미검증입니다.

## 지원 정책 정정·최소 환경 복원

최신화 요청은 테스트 환경의 최신 HA·플러그인을 뜻하며 컴포넌트 지원 하한 상승을 뜻하지 않습니다. `hacs.json`·README는 기존 최소 HA2025.3.0으로 복원했고, 최신 테스트는 HA2026.10.2/플러그인0.13.373으로 유지합니다. 최소 HA2025.3.0은 호환 플러그인0.13.221/Python3.13·공식 helper constraints와 함께 별도 job으로 복원했습니다. 실제 설치값은 해당 환경의 요구사항과 일치하고 현재 테스트 HA는 지원 하한 이상인지 검사합니다. Dependabot은 historical requirements/constraints를 제외하고 최신 환경 그룹만 갱신합니다. PR #8 merged 및 #9~12 obsolete closed라는 사실은 이력으로 남기며, 정정 구현은 별도 독립·원격 검증으로 판정합니다.

2026-10-17 `/root/review_kibble_pilot`은 지원 하한 복원 작업을 이전 PR #8과 분리해 재검증했습니다. 최신 환경 HA2026.10.2/플러그인0.13.373/Python3.14.5와 최소 환경 HA2025.3.0/플러그인0.13.221/Python3.13.14에서 각각 실제 HA 31 passed·pip check·Ruff·format을 통과했습니다. 지원 하한과 최신 테스트 분리, 두 환경별 실제 설치값, 역사적 최소 파일의 Dependabot 제외, 문서 정정과 중앙 기준 `103124f47c6fc838a39eddbd008e64cfb1a5e5f0` 고정을 확인합니다. 최종 정정 커밋 `f1a70396bea833b25e8fbcac7fa837ac3769ec91`의 원격 CI 성공과 중앙 종료 보고 등록을 아래에서 확인했습니다.

## 최종 지원 하한 복원 검증

실제 최종 구현 커밋은 `f1a70396bea833b25e8fbcac7fa837ac3769ec91`입니다. [Tests 39034355878](https://github.com/eigger/hass-kibble/actions/runs/39034355878)에서 최소 환경 Python3.13.16/HA2025.3.0/플러그인0.13.221은 31 passed(1.47초), 현재 환경 Python3.14.8/HA2026.10.2/플러그인0.13.373은 31 passed(1.29초)로 성공했습니다. 양쪽 pip check와 Ruff·format도 통과했습니다. [Validate 39034355875](https://github.com/eigger/hass-kibble/actions/runs/39034355875)는 HACS 9/9와 Hassfest를 통과했습니다. 독립 리뷰 담당이 실제 커밋·run·로그를 확인했습니다.

중앙 `4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28`은 이 구현과 검증의 종료 보고를 실제 등록한 커밋입니다. 이 문서 마감은 검증 대상 구현과 구분한 후속 문서 변경이며 자기 커밋을 사전에 검증했다고 기록하지 않습니다. 중앙 표 상태 완료 전환과 문서 마감 커밋 연결만 후속으로 처리합니다.
