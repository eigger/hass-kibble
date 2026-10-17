# 적용한 공통 규칙

- 표준: https://github.com/eigger/hass-repo-standards/tree/422115af66c329a9617e10a11cd321acc4221e13
- 참조 커밋 SHA: `422115af66c329a9617e10a11cd321acc4221e13`
- 채택일: 2026-10-17
- profile: integration / ha
- 기본 브랜치: master; domain: kibble
- 적용 점검표: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md)
- 중앙 현황표: https://github.com/eigger/hass-repo-standards/blob/main/docs/adoption-status.md
- 조율: /root; 구현: /root/implement_kibble_pilot; 독립 리뷰·검증: /root/review_kibble_pilot
- 중앙 현황 갱신: 주 에이전트가 최신 중앙 main에 기록
- 테스트 경로: `tests/components/kibble/`
- 현재 환경: Python 3.14 / HA 2026.10.2 / pytest-homeassistant-custom-component 0.13.373 (`requirements_test.txt`)
- 최소 환경: Python 3.13 / HA 2025.3.0 / pytest-homeassistant-custom-component 0.13.221 (`requirements_test_min.txt`)
- 최소 외부 라이브러리: 해당 없음 (`manifest.requirements=[]`)

## 검증 환경과 경계

실제 HA loader·config entry manager·플랫폼·flow·service·registry를 실행합니다. HTTP 응답만 플러그인의 `aioclient_mock`으로 대체하며, 기존 API 경계 단위 테스트도 보조로 유지합니다. HA 가짜 모듈과 FakeHass는 사용하지 않습니다. 구현된 센서·버튼과 기존 마지막 정상값 유지 계약은 보존하며 조회 오류 횟수로 오래된 값을 식별합니다. domain·entry schema·unique ID·단위·통계 계약·통합 버전은 변경하지 않습니다.

최소 HA 2025.3.0은 당시 HA 자체가 고정한 yanked `aiohttp==3.11.13`을 정확히 재현합니다. 이 버전은 회귀로 철회되었으며, 최소 환경 파일에만 명시합니다. 현재 환경은 HA 2026.10.2의 의존성 조합을 사용합니다. 최소 플러그인의 Bluetooth helper import가 요구하는 간접 패키지는 [당시 공식 Bluetooth manifest](https://github.com/home-assistant/core/blob/2025.3.0/homeassistant/components/bluetooth/manifest.json)의 여섯 버전을 `constraints/homeassistant-min.txt`에 고정합니다. 이는 테스트 환경 재현용이며 Kibble이 Bluetooth를 사용한다는 뜻이 아닙니다. `--no-deps`나 제약 무시는 사용하지 않습니다.

기기·운영 Kibble 서버와의 실물 검증은 수행하지 않았습니다. HACS·Hassfest 및 최종 커밋의 GitHub Actions 결과는 체크리스트에서 별도로 확인합니다.

## 예외

| 규칙 ID | 이유 | 담당자 | 재검토 조건 |
|---|---|---|---|
| GOV-03 | 사용자가 기존 대화에서 직접 push를 승인한 파일럿으로 채택 PR 대신 master 커밋·독립 리뷰·CI 증거를 기록 | eigger / /root | 이후 일반 채택 시 PR 경로 재검토 |

master branch protection 조회는 404(Branch not protected), rulesets는 빈 배열이므로 기존 required checks를 대기 상태로 만드는 설정 변경은 없습니다. 보안 설정은 변경하지 않습니다. 채택 작업으로 태그·Release를 만들지 않습니다.

## HACS brand asset

최초 Validate 실행에서 로컬 브랜드 자산과 HA brands 등록이 모두 없어 brands 검사만 실패했습니다. 기존 Kibble 프로젝트의 MIT 아이콘을 원본 그대로 `custom_components/kibble/brand/icon.png`에 제공했습니다. 출처·커밋·라이선스는 같은 폴더 README에 기록했으며 검사를 ignore하지 않습니다. 이는 HACS Default 또는 공식 HA brands 등록을 의미하지 않습니다.
