# 적용한 공통 규칙
- 표준: https://github.com/eigger/hass-repo-standards/tree/v1.0.0
- 참조 커밋 SHA: 44349ee5621eea5d80e5c427f7a2435d2c2491bb
- Standards release: v1.0.0
- Resolved standards SHA: 44349ee5621eea5d80e5c427f7a2435d2c2491bb
- 채택일: 2026-10-17
- profile: integration / ha
- 기본 브랜치: master; domain: kibble
- 적용 점검표: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md)
- 중앙 현황표: https://github.com/eigger/hass-repo-standards/blob/main/docs/adoption-status.md
- 조율: /root; 구현: /root/implement_kibble_pilot; 독립 리뷰·검증: /root/review_kibble_pilot
- 중앙 현황 갱신: 시작·단계·구현 검증 종료 보고 등록 완료 (`4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28`); 문서 마감 후 중앙 표 상태를 완료로 전환
- 테스트 경로: `tests/components/kibble/`
- 현재 테스트 환경: Python 3.14.2 이상 / HA 2026.10.2 / pytest-homeassistant-custom-component 0.13.373 (`requirements_test.txt`)
- 컴포넌트 지원 최소 환경: Python 3.13 / HA 2025.3.0 / pytest-homeassistant-custom-component 0.13.221 (`requirements_test_min.txt`)
- 최신 테스트 버전 갱신과 컴포넌트 지원 하한 변경을 구분하며, 이번 작업의 최종 지원 하한은 기존 2025.3.0을 유지
- 최소 외부 라이브러리: 해당 없음 (`manifest.requirements=[]`)

## 2026-10-23 공용 기준·ZIP 다운로드·브랜드 후속

이번 검토 기준은 `4ccbffa9af618b14d1a32a9939cbf1fcee6cb7a0`이며, 아래 2026-10-17 기록은 당시 구현·검증 이력입니다. 이번 변경은 로컬 작업 트리이며 과거 기본 브랜치 CI 성공과 구분합니다. 최신 중앙 main을 `git ls-remote`로 확인하고 별도 임시 checkout에서 검토했습니다. 기존 중앙 checkout의 사용자 수정은 보존했습니다.

- DOC-01~06: 중앙 생성기로 양언어 header/support/related-projects/license 및 설치 관리 영역을 적용했습니다. 기존 설치·기능·예제·상세 문서 본문을 유지하고 Downloads 의미만 배포 방식에 맞춰 정정했습니다.
- HACS-02~04: Custom 상태를 유지하며 `zip_release: true`, `filename: kibble.zip`과 중앙 Release caller를 추가했습니다. Downloads는 전체 릴리스 첨부 asset의 다운로드 합계이며 활성 설치 수가 아닙니다.
- GOV-02, CI-01~05: Tests/Validate/Release 및 준수 action을 검토 SHA로 고정하고 각 Tests job의 `standards-ref`를 일치시켰습니다. 최신 중앙 이벤트 계약에 따라 Tests의 주간 schedule은 제거하고 Validate의 주간 schedule을 월요일 03:23 UTC로 맞췄습니다. push/PR/수동 실행과 최소/current job은 유지합니다.
- HA-02: Kibble의 반려동물별 급여·체중·복약·케어 기록을 근거로 주 분류 `pets`를 선택했습니다. 엔티티 플랫폼에서 추정하지 않았으며 보조 분류는 없습니다. 분류와 판단은 `.hass-standards.json.categories_review`에 기록했습니다.
- TEST-03/08, HA-13: 빈 package init, 중앙 루트 fixture, domain fixture 관리 영역을 적용했습니다. 실제 기존 회귀 테스트는 보존합니다.
- HACS-05: stable Hassfest의 custom manifest categories 미지원에 대해 중앙의 공식 소스 빌드 경로를 사용합니다. `hassfest-core-ref: ec18d8b25d1ee39aa8b85a72a170e42bee33228c`는 실제 확인한 Core taxonomy·Dockerfile·entrypoint·manifest validator의 기준입니다. 검사를 제외하거나 manifest를 전처리하지 않습니다. 기본 공식 이미지가 해당 schema를 지원하면 이 입력을 제거하고 같은 대상에서 재검증합니다.
- 브랜드: 기존 아이콘 두 파일을 바이트 그대로 유지하고 투명 가로 로고 두 해상도를 추가했습니다. 출처·MIT·폰트 권리·재생성·해시는 `custom_components/kibble/brand/README.md`에 있습니다. README 양언어에 같은 로고를 표시합니다.

HA 지원 최소 2025.3.0/current 검증 2026.10.2, 통합 버전 0.1.5와 데이터 계약은 그대로입니다. 기존 Release 0.1.5에는 새 ZIP을 업로드하지 않았습니다. 이 설정이 원격에 반영되면 **변경을 포함하는 새 버전의 manifest와 일치하는 tag로 Release를 게시**해야 HACS ZIP 다운로드가 가능합니다. 새 Release 게시 이벤트가 ZIP을 첨부하며 기존 tag의 workflow/asset을 소급 변경하지 않습니다. 로컬 제공 ZIP은 검증용 작업 트리 스냅샷이고 새 정식 릴리스가 아닙니다.

이번 검증의 실제 명령·환경·결과·독립 리뷰·미검증은 [체크리스트의 후속 기록](ADOPTION_CHECKLIST.md#2026-10-23-공용-기준zip-다운로드브랜드-후속-검증)에 모았습니다. 원격 HACS/Actions·새 Release asset 다운로드·실물 서버·HA frontend 표시는 미검증입니다. 로컬 변경 검증을 전체 원격 재채택 완료로 기록하지 않습니다. 중앙 현황은 로컬 행만 갱신했고 원격 게시하지 않았습니다.

## 검증 환경과 경계

실제 HA loader·config entry manager·플랫폼·flow·service·registry를 실행합니다. HTTP 응답만 플러그인의 `aioclient_mock`으로 대체하며, 기존 API 경계 단위 테스트도 보조로 유지합니다. HA 가짜 모듈과 FakeHass는 사용하지 않습니다. 구현된 센서·버튼과 기존 마지막 정상값 유지 계약은 보존하며 조회 오류 횟수로 오래된 값을 식별합니다. domain·entry schema·unique ID·단위·통계 계약·통합 버전은 변경하지 않습니다.

`test_supported_environment.py`는 최소 테스트 HA가 `hacs.json`의 지원 하한과 정확히 일치하고 현재 테스트 HA가 그 하한 이상인지 확인합니다. 실제 설치된 HA와 플러그인은 각 환경의 정확한 requirements와 일치해야 합니다. 최신 환경의 HA·플러그인만 함께 갱신하며 그 이유만으로 컴포넌트 지원 최소를 올리지 않습니다. 사용자의 별도 지원 변경 요청이 있다면 사용자 영향·재검증·문서 변경을 함께 검토합니다. `--no-deps`나 제약 무시는 사용하지 않습니다.

최소 환경은 당시 HA 자체가 고정한 yanked `aiohttp==3.11.13`을 정확히 재현합니다. 이 버전은 회귀로 철회되었으며 최소 검증 파일에만 명시합니다. 최소 플러그인의 Bluetooth helper import용 간접 패키지는 [당시 공식 Bluetooth manifest](https://github.com/home-assistant/core/blob/2025.3.0/homeassistant/components/bluetooth/manifest.json)의 여섯 버전을 `constraints/homeassistant-min.txt`에 고정합니다. Kibble의 런타임 Bluetooth 의존성은 아닙니다. Dependabot의 `exclude-paths`로 이 역사적 최소 requirements와 constraints를 자동 갱신에서 제외하고 현재 HA·플러그인 그룹은 유지합니다.

기기·운영 Kibble 서버와의 실물 검증은 수행하지 않았습니다. HACS·Hassfest 및 최종 커밋의 GitHub Actions 결과는 체크리스트에서 별도로 확인합니다.

## 예외

현재 기록된 적용 예외는 없습니다. [PR #8](https://github.com/eigger/hass-kibble/pull/8)의 squash merge `e01ac2119c4ce571ffe82ab2b189173fc6c78b88`은 이전 채택과 일시적 지원 상향의 검증 이력입니다. 현재 검증 대상 구현은 지원 하한을 2025.3.0으로 복원한 `f1a70396bea833b25e8fbcac7fa837ac3769ec91`이며 독립·원격 검증을 완료했습니다. 이 문서 마감은 검증 대상 구현과 구분한 후속 변경입니다.

초기 파일럿은 사용자 승인에 따라 직접 master에 반영했던 이력이 있으며 당시 GOV-03 예외 기록을 남겼습니다. 이후 PR #8에서 최종 채택 전체를 명시적으로 검토·검증해 그 예외를 해제했습니다. 최초 직접 반영 사실을 소급해 PR 작업으로 바꾸는 것은 아닙니다.

master branch protection 조회는 404(Branch not protected), rulesets는 빈 배열이므로 기존 required checks를 대기 상태로 만드는 설정 변경은 없습니다. 보안 설정은 변경하지 않습니다. 채택 작업으로 태그·Release를 만들지 않습니다.

## HACS brand asset

최초 Validate 실행에서 로컬 브랜드 자산과 HA brands 등록이 모두 없어 brands 검사만 실패했습니다. 기존 Kibble 프로젝트의 MIT 512px 아이콘을 `custom_components/kibble/brand/icon@2x.png`에 원본 그대로 보존하고 HA 규격의 256px `icon.png`를 재현 가능한 LANCZOS 변환으로 제공했습니다. 출처·커밋·라이선스는 같은 폴더 README에 기록했으며 검사를 ignore하지 않습니다. 이는 HACS Default 또는 공식 HA brands 등록을 의미하지 않습니다.

로컬 brand의 HA UI 표시는 HA 2026.3부터 지원됩니다. 지원 최소 HA 2025.3.0의 로컬 아이콘 표시를 주장하지 않으며, 이번 PNG 파일 시각 검사와 HACS brands 검증은 실제 HA frontend UI 표시 검증을 의미하지 않습니다. 운영 Kibble 서버·실물 환경 검증도 수행하지 않았습니다.

## 지원 정책 정정과 릴리스 경계

PR #8에서 최신 테스트 갱신을 지원 하한 변경과 혼동해 HA 최소를 2026.10.2로 올렸던 상태를 정정했습니다. 최종 지원 하한은 기존 2025.3.0이며 최신 실제 HA 테스트 환경만 2026.10.2/플러그인0.13.373으로 유지합니다. 최소 환경도 별도로 복원·검증했습니다. domain·entry schema·unique ID는 그대로이므로 기존 설정과 통합 재등록에 관한 변경은 없습니다. 통합 버전·tag·GitHub Release는 만들지 않습니다.

## 이전 PR #8 검증 이력

[PR #8](https://github.com/eigger/hass-kibble/pull/8)을 squash merge한 구현 커밋 `e01ac2119c4ce571ffe82ab2b189173fc6c78b88`의 [Tests](https://github.com/eigger/hass-kibble/actions/runs/39033920073)와 [Validate](https://github.com/eigger/hass-kibble/actions/runs/39033920133)가 성공했습니다. 해당 커밋의 실제 HA 31개 테스트·pip check·Ruff·format·HACS·Hassfest 성공은 이전 검증 이력입니다. 이후 지원 정책 정정·최소 환경 복원의 최종 결과는 체크리스트에서 별도 확인합니다.

## 최종 적용 판정

적용 대상 필수 항목은 PASS 또는 이유가 있는 N/A이며 현재 예외는 없습니다. 실제 구현 커밋 `f1a70396bea833b25e8fbcac7fa837ac3769ec91`의 [Tests](https://github.com/eigger/hass-kibble/actions/runs/39034355878)는 최소·현재 실제 HA 환경 각각 31 passed·pip check·Ruff·format을 통과했고, [Validate](https://github.com/eigger/hass-kibble/actions/runs/39034355875)는 HACS 9/9·Hassfest를 통과했습니다. 독립 담당자가 확인한 종료 결과는 중앙 `4726ab1d5c93ff1af0e9aaead2bb1631d80e1f28`에 등록했습니다. 중앙 표의 상태 완료 전환은 문서 마감 이후 별도 행정 후속입니다. 실물·운영 서버와 HA frontend UI 미검증 한계는 그대로 유지합니다.

## README 언어·Usage 배지 정책 후속 반영 (2026-10-17)

영문은 [README.md](README.md)를 기본으로 제공하고 한국어 전체 문서는 [README.ko.md](README.ko.md)에 유지합니다. 종전 영문 경로 [README.en.md](README.en.md)는 기본 문서로 안내합니다. 두 언어의 상호 링크·설치 앵커·관리 배지 설정을 함께 유지하며, manifest domain `kibble`의 Usage 동적 배지는 사전 집계 확인이나 조회 성공을 조건으로 하지 않습니다. Analytics 참여 설치 집계라는 의미를 문서에 명시하고 미집계·조회 불가를 0으로 표현하지 않습니다. 지원 하한·테스트 환경·런타임·CI 실행 동작은 유지합니다. 새 기준 `7528a90b483a6740c0b1bdd9176f3e33355eb385`으로 세 caller의 SHA를 함께 갱신했으며, 이전 기준과 호출 workflow 내용이 동일한 문서·기준 고정 후속 작업입니다. 새 최종 커밋의 원격 CI 결과는 대기 중이며 위 구현 검증 이력과 구분합니다.

메인 README는 빠른 시작 중심으로 정리하고 상세 사용·오류 대응과 개발·테스트 안내는 영문 `docs/user-guide.md`·`docs/development.md`, 한국어 `docs/ko/`에 보존해 문서 표에서 연결합니다. 기존 언어별 설치·토큰·엔티티 속성·기록 보관·테스트 조합 안내를 삭제하지 않는 문서 분리입니다.

## 2026-10-23 릴리스 0.1.6

사용자의 릴리스 요청에 따라 통합 버전을 0.1.6으로 올려 위 공용화·ZIP 배포·브랜드 변경을 정식 배포합니다. 지원 최소 HA 2025.3.0은 유지합니다. 이전 절의 로컬 미게시 표기는 당시 검증 경계이며, 이 후속 릴리스의 실제 커밋·CI·ZIP 게시 결과는 체크리스트에 별도 기록합니다.
