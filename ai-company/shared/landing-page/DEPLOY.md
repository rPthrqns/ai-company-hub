# 배포 가이드

## 1. Netlify (추천)

```bash
# 방법 A: 드래그 앤 드롭
# https://app.netlify.com/drop 에 landing-page/ 폴더 드래그

# 방법 B: CLI
npm install -g netlify-cli
cd landing-page
netlify deploy --prod --dir=.
```

폼 처리를 원하면 `index.html`의 `<form>`에 `data-netlify="true"` 추가.

## 2. Vercel

```bash
npm i -g vercel
cd landing-page
vercel --prod
```

## 3. GitHub Pages

1. 레포지토리에 `landing-page/` 푸시
2. Settings → Pages → Source: Deploy from branch → `main` / `/(root)`
3. URL: `https://username.github.io/repo/`

## 4. AWS S3 + CloudFront

```bash
aws s3 sync ./landing-page/ s3://your-bucket/ --delete
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

## 5. 자체 서버 (Nginx)

```nginx
server {
    listen 80;
    server_name recruit.example.com;
    root /var/www/landing-page;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 도메인 연결

배포 후 DNS 설정:
- CNAME 레코드 생성: `recruit` → 배포 플랫폼 도메인
- SSL은 Netlify/Vercel에서 자동 발급

## 배포 전 체크리스트

- [ ] SEO 메타 태그 확인 (og:image 경로 절대 URL로 변경)
- [ ] 폼 제출 처리 연동 (Netlify Forms / API / 이메일 서비스)
- [ ] og-image.jpg 생성 (1200x630px 권장)
- [ ] 실제 연락처/이메일로 변경
- [ ] 분석 도구 연동 (Google Analytics / NAVER Analytics)
- [ ] robots.txt 추가 (필요시)
- [ ] 모바일 테스트 완료
