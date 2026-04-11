from parsers.categories import detect_category


def test_dev():
    assert detect_category("API 서버 구축") == 'dev'
    assert detect_category("Backend deploy") == 'dev'
    assert detect_category("DB 스키마 설계") == 'dev'


def test_design():
    assert detect_category("로고 디자인") == 'design'
    assert detect_category("UI 시안 작업") == 'design'
    assert detect_category("Mockup creation") == 'design'


def test_marketing():
    assert detect_category("SNS 광고 캠페인") == 'market'
    assert detect_category("SEO 최적화") == 'market'
    assert detect_category("브랜딩 전략") == 'market'  # 브랜딩 takes precedence


def test_ops():
    assert detect_category("예산 편성") == 'ops'
    assert detect_category("HR 채용 정책") == 'ops'


def test_plan_default():
    assert detect_category("시장 조사") == 'plan'
    assert detect_category("전략 수립") == 'plan'
    assert detect_category("그냥 무언가") == 'plan'


def test_empty():
    assert detect_category("") == 'plan'
    assert detect_category(None) == 'plan'
