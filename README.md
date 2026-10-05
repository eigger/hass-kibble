# Kibble Home Assistant Integration (hass-kibble)

[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat-square&label=tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![GitHub Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat-square)](https://github.com/eigger/hass-kibble/releases)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat-square)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Kibble을 Home Assistant에 **읽기 전용**으로 연결하는 커스텀 통합입니다. Kibble 서버의 오늘 요약, 마지막 기록, 복약 지연 및 리마인더를 5분마다 읽어 센서로 표시합니다.

## 설치

1. Home Assistant 2025.3 이상에서 HACS의 사용자 지정 저장소에 `eigger/hass-kibble`을 **Integration**으로 추가합니다.
2. 통합을 설치하고 Home Assistant를 재시작합니다.
3. **설정 → 기기 및 서비스 → 통합 추가 → Kibble**을 선택합니다.
4. Kibble 서버 주소와 해당 반려동물에 고정된 `state:read` API 토큰을 입력합니다.

Kibble 웹의 **설정 → 외부 연동 토큰**에서 반려동물을 선택해 읽기 전용 토큰을 발급할 수 있습니다. 원문은 발급 직후에만 표시되므로 바로 복사하세요.

## 엔티티

- **오늘 기록 수**: 오늘 발생한 기록의 전체 횟수. 이벤트 유형별 횟수와 단위별 합계는 이 센서의 `today_summary` 속성에 표시됩니다.
- **복약 지연 횟수**: 예정 시각이 지난 미기록 복약 횟수와 대상 과정.
- **리마인더**: 활성 리마인더 수와 상세 목록.
- **지금 새로고침** 버튼: 다음 주기를 기다리지 않고 즉시 Kibble에 다시 요청합니다.

이벤트 종류별 센서는 그 종류의 마지막 기록을 기준으로 만들어져 자정 이후 재시작해도 유지됩니다. 상세 값은 오늘 기록 수 센서의 `today_summary`, `last_events`, `medication`, `reminders` 속성에 제공됩니다. 이전 서버 응답은 간략한 `today` 집계를 이용해 가능한 수량을 표시합니다.

기본 갱신 주기는 5분입니다. 인증 실패는 통합의 재인증 흐름으로 안내됩니다. 이 통합은 Kibble에 데이터를 쓰지 않습니다.

## 개발

```sh
pip install pytest ruff aiohttp
python -m ruff check custom_components/ tests/
python -m pytest tests/ -v
```
