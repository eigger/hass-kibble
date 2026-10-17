# 적용한 공통 규칙

- 표준: https://github.com/eigger/hass-repo-standards/tree/a6deb61613407c099b28cbbe826ba89be1464e7d
- 참조 커밋 SHA: `a6deb61613407c099b28cbbe826ba89be1464e7d`
- 채택일: 2026-10-17
- profile: integration / ha
- 기본 브랜치: master; domain: kibble
- 적용 점검표: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md)
- 중앙 현황표: https://github.com/eigger/hass-repo-standards/blob/main/docs/adoption-status.md
- 조율: /root; 구현: /root/implement_kibble_pilot; 독립 리뷰·검증: /root/review_kibble_pilot
- 중앙 현황 갱신: 주 에이전트가 최신 중앙 main에 기록
- 테스트 경로: `tests/components/kibble/`
- 현재 환경 = 정확한 최소 지원 환경: Python 3.14.2 이상 / HA 2026.10.2 / pytest-homeassistant-custom-component 0.13.373 (`requirements_test.txt`)
- 지원 정책 변경: 사용자 요청으로 HA 최소 버전을 2025.3.0에서 2026.10.2로 상향하고 구 최소 환경·requirements·constraints를 제거
- 최소 외부 라이브러리: 해당 없음 (`manifest.requirements=[]`)

## 검증 환경과 경계

실제 HA loader·config entry manager·플랫폼·flow·service·registry를 실행합니다. HTTP 응답만 플러그인의 `aioclient_mock`으로 대체하며, 기존 API 경계 단위 테스트도 보조로 유지합니다. HA 가짜 모듈과 FakeHass는 사용하지 않습니다. 구현된 센서·버튼과 기존 마지막 정상값 유지 계약은 보존하며 조회 오류 횟수로 오래된 값을 식별합니다. domain·entry schema·unique ID·단위·통계 계약·통합 버전은 변경하지 않습니다.

`hacs.json`의 최소 HA와 정확히 고정한 테스트 HA 및 실제 설치 HA 버전을 `test_supported_environment.py`에서 함께 확인합니다. 현재 테스트 버전이 최소 지원 버전과 같아 한 환경으로 실제 최소 HA 검증도 수행합니다. Dependabot은 남은 현재 HA·플러그인 조합을 묶어 제안하며, HA 버전 변경 시 `hacs.json`·workflow의 expected HA·README·검증 기록도 함께 갱신해야 합니다. 최소 지원 변경을 포함한 PR은 사용자 영향과 조치 안내를 갱신하지 않은 채 병합하지 않습니다. `--no-deps`나 제약 무시는 사용하지 않습니다.

초기 파일럿에서는 과거 최소 HA 2025.3.0을 별도 검증했지만 이는 이전 커밋의 이력입니다. 해당 환경과 역사적 yanked 의존성 pin은 현재 브랜치에서 제거했습니다.

기기·운영 Kibble 서버와의 실물 검증은 수행하지 않았습니다. HACS·Hassfest 및 최종 커밋의 GitHub Actions 결과는 체크리스트에서 별도로 확인합니다.

## 예외

| 규칙 ID | 이유 | 담당자 | 재검토 조건 |
|---|---|---|---|
| GOV-03 | 사용자가 기존 대화에서 직접 push를 승인한 파일럿으로 채택 PR 대신 master 커밋·독립 리뷰·CI 증거를 기록 | eigger / /root | 이후 일반 채택 시 PR 경로 재검토 |

master branch protection 조회는 404(Branch not protected), rulesets는 빈 배열이므로 기존 required checks를 대기 상태로 만드는 설정 변경은 없습니다. 보안 설정은 변경하지 않습니다. 채택 작업으로 태그·Release를 만들지 않습니다.

## HACS brand asset

최초 Validate 실행에서 로컬 브랜드 자산과 HA brands 등록이 모두 없어 brands 검사만 실패했습니다. 기존 Kibble 프로젝트의 MIT 512px 아이콘을 `custom_components/kibble/brand/icon@2x.png`에 원본 그대로 보존하고 HA 규격의 256px `icon.png`를 재현 가능한 LANCZOS 변환으로 제공했습니다. 출처·커밋·라이선스는 같은 폴더 README에 기록했으며 검사를 ignore하지 않습니다. 이는 HACS Default 또는 공식 HA brands 등록을 의미하지 않습니다.

로컬 brand의 HA UI 표시는 HA 2026.3부터 지원됩니다. 초기 파일럿에서 사용했던 HA 2025.3.0의 로컬 아이콘 표시를 주장하지 않으며, 이번 PNG 파일 시각 검사와 HACS brands 검증은 실제 HA frontend UI 표시 검증을 의미하지 않습니다. 운영 Kibble 서버·실물 환경 검증도 수행하지 않았습니다.

## 지원 변경과 릴리스 경계

사용자 요청으로 최소 HA를 2026.10.2로 상향했습니다. 이전 HA 사용자는 이 변경이 포함된 버전 설치 전 HA를 업데이트해야 합니다. domain·entry schema·unique ID는 그대로이므로 통합 재등록은 필요하지 않습니다. 이 사용자 조치는 두 언어 README에 기록했습니다. 이번 작업으로 통합 버전·tag·GitHub Release는 자동 생성하지 않습니다. 실제 다음 릴리스에서는 기존 버전 정책에 따라 지원 상향을 버전과 release notes에 반영하고 동일 커밋 검증을 확인해야 합니다.
