# Kibble Home Assistant Integration (hass-kibble)

[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat-square&label=tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![GitHub Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat-square)](https://github.com/eigger/hass-kibble/releases)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat-square)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Kibble을 Home Assistant에 **읽기 전용**으로 연결하는 커스텀 통합입니다. Kibble 서버의 오늘 요약, 개별 제공·섭취 및 케어 기록, 복약 지연 및 리마인더를 5분마다 읽어 센서로 표시합니다.

## 설치

1. Home Assistant 2025.3 이상에서 HACS의 사용자 지정 저장소에 `eigger/hass-kibble`을 **Integration**으로 추가합니다.
2. 통합을 설치하고 Home Assistant를 재시작합니다.
3. **설정 → 기기 및 서비스 → 통합 추가 → Kibble**을 선택합니다.
4. Kibble 서버 주소와 해당 반려동물에 고정된 `state:read` API 토큰을 입력합니다.

Kibble 웹의 **더보기 → API 탐색기 → 외부 연동 토큰**에서 반려동물을 선택해 읽기 전용 토큰을 발급할 수 있습니다. 원문은 발급 직후에만 표시되므로 바로 복사하세요.

## 엔티티

- **오늘 기록 수**: 오늘 발생한 기록의 전체 횟수. 이벤트 유형별 횟수와 단위별 합계는 이 센서의 `today_summary` 속성에 표시됩니다.
- **일일 기록 목록**: 같은 센서의 `today_events` 속성에 시각, 기록 종류, 제공·섭취량, 품목/프리셋, 메모 및 복약 과정을 최신순으로 표시합니다. 최대 100건이며 초과 여부는 `today_events_truncated`로 알립니다.
- **일일 누계 센서**: 오늘 기록 수, 유형별 기록 수, 사료 제공·섭취량 및 물 섭취량은 Kibble의 오늘 경계를 기준으로 초기화되는 누계로 표시합니다.
- **현재 측정 센서**: 체중은 가장 최근 기록, 복약 지연 및 리마인더는 현재 개수로 표시합니다.
- **복약 지연 횟수**: 예정 시각이 지난 미기록 복약 횟수와 대상 과정.
- **리마인더**: 활성 리마인더 수와 상세 목록.
- **연속 조회 오류 횟수**: 그래프에서 연속 실패 횟수를 볼 수 있습니다. `last_error`, `last_error_at`, `last_success_at` 속성에 최근 오류와 정상 조회 시각을 표시합니다.
- **지금 새로고침** 버튼: 다음 주기를 기다리지 않고 즉시 Kibble에 다시 요청합니다.

이벤트 종류별 센서는 그 종류의 마지막 기록을 기준으로 만들어져 자정 이후 재시작해도 유지됩니다. 관리 정보는 오늘 기록 수 센서의 `medication`, `reminders` 속성과 `today_events` 목록에 제공됩니다. 이 큰 상세 속성은 HA 기록기 저장에서 제외되어 현재 대시보드에는 표시되지만 과거 속성으로 보관되지는 않습니다. 숫자 센서는 정상적으로 기록됩니다. 이전 서버 응답은 간략한 `today` 집계를 이용해 가능한 수량을 표시합니다.

기본 갱신 주기는 5분입니다. 조회에 실패하면 마지막 정상 데이터를 유지하고 연속 오류 횟수를 올립니다. 다음 정상 조회가 성공하면 오류 횟수는 0으로 돌아갑니다. 인증 실패 시에도 기존 값을 유지하면서 재인증 흐름을 시작합니다. 이 통합은 Kibble에 데이터를 쓰지 않습니다.

## 개발

```sh
pip install pytest ruff aiohttp
python -m ruff check custom_components/ tests/
python -m pytest tests/ -v
```
