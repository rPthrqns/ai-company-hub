# 삼성화재 보험설계사 모집 랜딩페이지

## 기술 스택 선정

### 채택: 순수 HTML/CSS/JS (정적 사이트)

**이유:**
- **랜딩페이지 = 단일 페이지** → SPA 프레임워크 불필요
- **SEO 최우선** → SSR 없이도 정적 HTML이 크롤러에 최적
- **빠른 로딩** → JS 번들링 없이 순수 CSS, 0KB JS 프레임워크 오버헤드
- **유지보수 간단** → 디자이너도 수정 가능한 구조
- **호스팅 비용 최소화** → Netlify/Vercel/GitHub Pages 무료 배포 가능

### Next.js를 추천하지 않은 이유:
- React hydration 오버헤드 (~100KB+)
- 단일 랜딩페이지에 과한 도구
- 정적 내용에 SSR 이점 없음
- 빌드 파이프라인 복잡도 불필요

> **단,** 향후 여러 랜딩페이지 관리 / CMS 연동 / A/B 테스트가 필요해지면 Next.js 도입 검토.

## 프로젝트 구조

```
landing-page/
├── index.html              # 메인 랜딩페이지
├── assets/
│   ├── css/
│   │   └── style.css       # 전체 스타일 (반응형 포함)
│   ├── js/
│   │   └── main.js         # 탭, 폼, 네비게이션 인터랙션
│   └── images/             # 이미지 (og-image.jpg 등)
└── DEPLOY.md               # 배포 가이드
```

## 포함된 섹션

1. **히어로** - 메인 카피 + CTA + 통계
2. **혜택** - 6개 혜택 카드 그리드
3. **지원 자격** - 신규/경력직 탭 전환
4. **지원 절차** - 4단계 프로세스
5. **지원 폼** - 이름, 연락처, 이메일, 구분, 경력, 근무지, 메시지
6. **CTA 배너**
7. **푸터**

## 주요 기능

- ✅ 반응형 디자인 (모바일/태블릿/데스크톱)
- ✅ SEO 메타 태그 (OG, Twitter Card, robots)
- ✅ 전화번호 자동 포맷팅
- ✅ 폼 유효성 검사
- ✅ 모바일 플로팅 CTA
- ✅ 스크롤 헤더 효과
- ✅ 부드러운 스크롤

## 로컬 개발

```bash
# Python
cd landing-page && python3 -m http.server 8000

# Node
npx serve landing-page

# VS Code Live Server 확장 사용
```

브라우저에서 `http://localhost:8000` 열기

## 폼 백엔드 연동

현재 폼은 `console.log`로 데이터를 출력합니다. 실제 운영 시:

1. **Netlify Forms** - HTML에 `netlify` 속성 추가
2. **Google Forms 연동** - Zapier/Make로 연결
3. **자체 API** - `fetch('/api/apply', { method: 'POST', body: formData })`
4. **이메일 전송** - EmailJS 또는 Formspree 사용
