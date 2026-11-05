<!-- hass-standards:header:start -->
# Kibble for Home Assistant

Kibble 반려동물 케어 기록을 읽기 전용으로 연결하는 Home Assistant 커스텀 통합입니다.

[English](README.md) | **한국어**

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-kibble?style=flat)](https://github.com/eigger/hass-kibble/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#설치)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.3.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-kibble/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-kibble/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-kibble/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-kibble?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-kibble/latest/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-kibble/releases)
<!-- hass-standards:badges:end -->
<!-- hass-standards:header:end -->

![Kibble](custom_components/kibble/brand/logo.png)

Kibble을 Home Assistant에 **읽기 전용**으로 연결하는 커스텀 통합입니다. Kibble 서버의 오늘 요약, 개별 제공·섭취 및 케어 기록, 복약 지연 및 리마인더를 5분마다 읽어 센서로 표시합니다.

## 주요 기능

- 오늘의 급여·섭취·케어 기록과 복약 지연·리마인더 센서
- 일일 누계·체중과 상세 기록 속성
- 연속 조회 오류 횟수와 지금 새로고침 버튼

## 요구사항

- **Home Assistant:** 2025.3.0 이상.
- **서버:** 로컬 HTTP 또는 HTTPS로 접속할 수 있는 Kibble 서버.
- **API 토큰:** 반려동물별 `state:read` 토큰.

## 설치

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-kibble&category=integration)
<!-- hass-standards:installation:end -->

1. 위 배지를 클릭해 마켓플레이스에서 저장소를 엽니다.
2. 저장소를 직접 추가하려면 **설정 → 마켓플레이스 → 링크에서 추가**에서 <https://github.com/eigger/hass-kibble>을 입력합니다. 안내가 표시되면 GitHub 계정을 연결합니다.
3. **설치**를 선택합니다. 재시작 안내가 표시되면 Home Assistant를 재시작합니다. 설치가 끝나면 [설정](#설정)으로 이동합니다.

## 설정

1. **설정 → 기기 및 서비스 → 통합 추가 → Kibble**을 선택합니다.
2. 서버 주소와 반려동물별 `state:read` 토큰을 입력합니다.

[토큰 발급 안내](docs/ko/user-guide.md#설치)를 참고하세요.

## 사용 예시

```yaml
action: button.press
target:
  entity_id: button.bori_refresh_now
```

실제 설치에서 생성된 새로고침 버튼의 엔티티 ID를 사용하세요.

이 통합은 **읽기 전용**입니다. 오류 중에도 마지막 정상값이 남으므로 연속 조회 오류 횟수를 함께 확인하세요. [자세한 문제 해결](docs/ko/user-guide.md#제한과-문제-해결)

## 문서

| 안내 | 내용 |
|---|---|
| [사용 안내](docs/ko/user-guide.md) | 설정·토큰, 엔티티/속성, 기록 보관, 오류 대응, Downloads 집계 의미 |
| [개발과 테스트](docs/ko/development.md) | 실제 HA 테스트, 최소·최신 환경, 의존성과 실행 명령 |
| [적용 기준](STANDARDS.md) · [체크리스트](ADOPTION_CHECKLIST.md) | 공통 규칙과 검증 기록 |

<!-- hass-standards:support:start -->
## 지원

- [Issues](https://github.com/eigger/hass-kibble/issues): 버그를 신고하거나 기능을 요청하세요.
- [Discussions](https://github.com/eigger/hass-kibble/discussions): 질문하고 사용 경험을 공유하세요.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
## 관련 프로젝트

- [Kibble](https://github.com/eigger/kibble): 이 통합이 연결하는 반려동물 케어 서버이자 브랜드 아이콘의 원본입니다.
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## 라이선스

[MIT License](LICENSE) 라이선스로 배포됩니다.
<!-- hass-standards:license:end -->
