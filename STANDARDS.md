# 적용한 공통 규칙

- 표준: https://github.com/eigger/hass-repo-standards/tree/103124f47c6fc838a39eddbd008e64cfb1a5e5f0
- 참조 커밋 SHA: `103124f47c6fc838a39eddbd008e64cfb1a5e5f0`
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
