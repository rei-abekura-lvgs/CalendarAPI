/**
 * 詳細四柱推命運勢診断API
 * 生年月日時間・性別を使った本格的な運勢計算
 */

class DetailedFortuneAPI {
    constructor() {
        this.detailedCache = new Map();
    }

    /**
     * 年月日時間選択肢の初期化
     */
    initializeDateSelectors() {
        // 年選択肢（1940年〜2010年）
        const yearSelect = document.getElementById('birthYear');
        if (yearSelect && yearSelect.children.length <= 1) {
            for (let year = 2010; year >= 1940; year--) {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = year + '年';
                yearSelect.appendChild(option);
            }
        }

        // 時間選択肢（0〜23時）
        const hourSelect = document.getElementById('birthHour');
        if (hourSelect && hourSelect.children.length <= 2) {
            for (let hour = 0; hour <= 23; hour++) {
                const option = document.createElement('option');
                option.value = hour;
                option.textContent = hour + '時';
                hourSelect.appendChild(option);
            }
        }

        // 日選択肢の動的更新
        const monthSelect = document.getElementById('birthMonth');
        const daySelect = document.getElementById('birthDay');
        
        if (monthSelect && daySelect) {
            monthSelect.addEventListener('change', () => {
                this.updateDayOptions();
            });
            
            const yearSelect = document.getElementById('birthYear');
            if (yearSelect) {
                yearSelect.addEventListener('change', () => {
                    this.updateDayOptions();
                });
            }
        }
    }

    /**
     * 日選択肢の動的更新（月・年に応じて）
     */
    updateDayOptions() {
        const yearSelect = document.getElementById('birthYear');
        const monthSelect = document.getElementById('birthMonth');
        const daySelect = document.getElementById('birthDay');
        
        if (!yearSelect || !monthSelect || !daySelect) return;
        
        const year = parseInt(yearSelect.value);
        const month = parseInt(monthSelect.value);
        
        if (!year || !month) return;
        
        // 月の日数を計算
        const daysInMonth = new Date(year, month, 0).getDate();
        
        // 既存の選択肢をクリア
        daySelect.innerHTML = '<option value="">日を選択</option>';
        
        // 新しい日選択肢を追加
        for (let day = 1; day <= daysInMonth; day++) {
            const option = document.createElement('option');
            option.value = day;
            option.textContent = day + '日';
            daySelect.appendChild(option);
        }
    }

    /**
     * 詳細運勢診断メイン関数
     */
    async calculateDetailedFortune() {
        const birthData = this.getBirthInputData();
        
        if (!this.validateInput(birthData)) {
            return null;
        }

        const cacheKey = this.generateCacheKey(birthData);
        
        if (this.detailedCache.has(cacheKey)) {
            return this.detailedCache.get(cacheKey);
        }

        try {
            // 今日のデータを取得
            const today = new Date();
            const todayData = await this.getTodayData();
            
            if (!todayData) throw new Error('今日のデータ取得失敗');

            // 四柱推命計算
            const fourPillars = this.calculateFourPillars(birthData);
            
            // 性別による補正
            const genderModifier = this.calculateGenderModifier(birthData.gender, fourPillars);
            
            // 今日との相性計算
            const todayCompatibility = this.calculateTodayCompatibility(fourPillars, todayData);
            
            // 大運・流年計算
            const daiun = this.calculateDaiun(fourPillars, birthData.gender);
            const ryunen = this.calculateRyunen(fourPillars, today.getFullYear());
            
            // 総合運勢計算
            const detailedFortune = this.calculateComprehensiveFortune(
                fourPillars, 
                genderModifier, 
                todayCompatibility, 
                daiun, 
                ryunen,
                todayData
            );

            // キャッシュに保存
            this.detailedCache.set(cacheKey, detailedFortune);
            
            return detailedFortune;
            
        } catch (error) {
            console.error('詳細運勢診断エラー:', error);
            return null;
        }
    }

    /**
     * 入力データ取得
     */
    getBirthInputData() {
        const year = document.getElementById('birthYear')?.value;
        const month = document.getElementById('birthMonth')?.value;
        const day = document.getElementById('birthDay')?.value;
        const hour = document.getElementById('birthHour')?.value || 'unknown';
        const minute = document.getElementById('birthMinute')?.value || 0;
        const gender = document.querySelector('input[name="gender"]:checked')?.value;

        return {
            year: parseInt(year),
            month: parseInt(month),
            day: parseInt(day),
            hour: hour === 'unknown' ? 'unknown' : parseInt(hour),
            minute: parseInt(minute),
            gender: gender
        };
    }

    /**
     * 入力検証
     */
    validateInput(birthData) {
        return birthData.year && birthData.month && birthData.day && birthData.gender;
    }

    /**
     * キャッシュキー生成
     */
    generateCacheKey(birthData) {
        return `${birthData.year}-${birthData.month}-${birthData.day}-${birthData.hour}-${birthData.gender}`;
    }

    /**
     * 今日のデータ取得
     */
    async getTodayData() {
        try {
            const today = new Date();
            const year = today.getFullYear();
            const month = (today.getMonth() + 1).toString().padStart(2, '0');
            
            const response = await fetch(`api/${year}/${month}.json`);
            if (!response.ok) throw new Error('APIレスポンスエラー');
            
            const monthData = await response.json();
            const day = today.getDate();
            
            return monthData.days.find(dayData => dayData.day === day);
        } catch (error) {
            console.error('今日のデータ取得エラー:', error);
            return null;
        }
    }

    /**
     * 四柱推命計算（年月日時の四柱）
     */
    calculateFourPillars(birthData) {
        const year = this.calculateYearPillar(birthData.year);
        const month = this.calculateMonthPillar(birthData.year, birthData.month);
        const day = this.calculateDayPillar(new Date(birthData.year, birthData.month - 1, birthData.day));
        const hour = birthData.hour !== 'unknown' ? 
            this.calculateHourPillar(day.kan, birthData.hour) : null;

        return { year, month, day, hour };
    }

    /**
     * 年柱計算
     */
    calculateYearPillar(year) {
        const kanshi = this.getYearKanshi(year);
        const kan = kanshi.charAt(0);
        const shi = kanshi.charAt(1);
        
        return {
            kanshi: kanshi,
            kan: kan,
            shi: shi,
            element: this.getElementFromKan(kan),
            yinYang: this.getYinYangFromKan(kan),
            animal: this.getAnimalFromShi(shi)
        };
    }

    /**
     * 月柱計算
     */
    calculateMonthPillar(year, month) {
        const kanshi = this.getMonthKanshi(year, month);
        const kan = kanshi.charAt(0);
        const shi = kanshi.charAt(1);
        
        return {
            kanshi: kanshi,
            kan: kan,
            shi: shi,
            element: this.getElementFromKan(kan),
            yinYang: this.getYinYangFromKan(kan),
            animal: this.getAnimalFromShi(shi)
        };
    }

    /**
     * 日柱計算
     */
    calculateDayPillar(birthDate) {
        const kanshi = this.getDayKanshi(birthDate);
        const kan = kanshi.charAt(0);
        const shi = kanshi.charAt(1);
        
        return {
            kanshi: kanshi,
            kan: kan,
            shi: shi,
            element: this.getElementFromKan(kan),
            yinYang: this.getYinYangFromKan(kan),
            animal: this.getAnimalFromShi(shi)
        };
    }

    /**
     * 時柱計算
     */
    calculateHourPillar(dayKan, hour) {
        const kanOrder = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shiOrder = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        const dayKanIndex = kanOrder.indexOf(dayKan);
        const hourShi = shiOrder[Math.floor(hour / 2)];
        
        // 簡易計算
        const hourKanIndex = (dayKanIndex * 2 + Math.floor(hour / 2)) % 10;
        const hourKan = kanOrder[hourKanIndex];
        const kanshi = hourKan + hourShi;
        
        return {
            kanshi: kanshi,
            kan: hourKan,
            shi: hourShi,
            element: this.getElementFromKan(hourKan),
            yinYang: this.getYinYangFromKan(hourKan),
            animal: this.getAnimalFromShi(hourShi)
        };
    }

    /**
     * 性別による補正計算
     */
    calculateGenderModifier(gender, fourPillars) {
        const baseModifier = gender === 'female' ? 1.05 : 0.95;
        
        // 五行による補正
        const dayElement = fourPillars.day.element;
        let elementModifier = 1.0;
        
        if (gender === 'female') {
            switch (dayElement) {
                case '水': elementModifier = 1.1; break;
                case '木': elementModifier = 1.05; break;
                case '土': elementModifier = 1.0; break;
                case '金': elementModifier = 0.95; break;
                case '火': elementModifier = 0.9; break;
            }
        } else {
            switch (dayElement) {
                case '火': elementModifier = 1.1; break;
                case '金': elementModifier = 1.05; break;
                case '土': elementModifier = 1.0; break;
                case '木': elementModifier = 0.95; break;
                case '水': elementModifier = 0.9; break;
            }
        }
        
        return baseModifier * elementModifier;
    }

    /**
     * 今日との相性計算
     */
    calculateTodayCompatibility(fourPillars, todayData) {
        let compatibility = 50;
        
        // 干支による相性
        const dayElement = fourPillars.day.element;
        const todayElement = this.getTodayElement(todayData);
        
        if (this.isCompatibleElements(dayElement, todayElement)) {
            compatibility += 20;
        } else if (this.isConflictingElements(dayElement, todayElement)) {
            compatibility -= 15;
        }
        
        // ランダム要素を追加（実際の四柱推命はより複雑）
        compatibility += Math.floor(Math.random() * 20) - 10;
        
        return Math.max(10, Math.min(90, compatibility));
    }

    /**
     * 大運計算（10年運）
     */
    calculateDaiun(fourPillars, gender) {
        const currentYear = new Date().getFullYear();
        const birthYear = fourPillars.year;
        const age = currentYear - parseInt(birthYear.kanshi.match(/\d+/)?.[0] || '2000');
        
        const startAge = this.calculateDaiunStartAge(fourPillars.month, gender);
        const period = Math.floor((age - startAge) / 10);
        
        return {
            period: period,
            startAge: startAge + (period * 10),
            endAge: startAge + ((period + 1) * 10) - 1,
            description: this.getDaiunDescription(period, fourPillars.day.element)
        };
    }

    /**
     * 流年計算（年運）
     */
    calculateRyunen(fourPillars, currentYear) {
        const yearKanshi = this.getYearKanshi(currentYear);
        const yearElement = this.getElementFromKan(yearKanshi.charAt(0));
        const dayElement = fourPillars.day.element;
        
        const relationship = this.analyzeElementRelationship(dayElement, yearElement);
        const fortune = this.calculateRyunenFortune(relationship);
        
        return {
            year: currentYear,
            pillar: {
                kanshi: yearKanshi,
                element: yearElement
            },
            relationship: relationship,
            fortune: fortune
        };
    }

    /**
     * 総合運勢計算
     */
    calculateComprehensiveFortune(fourPillars, genderModifier, todayCompatibility, daiun, ryunen, todayData) {
        // 基本スコア計算
        const baseScores = this.calculateBaseScores(todayData);
        
        // 個人修正値計算
        const personalModifier = this.calculatePersonalModifier(todayData, fourPillars);
        
        // 大運・流年修正
        const periodModifier = this.calculatePeriodModifier(daiun, ryunen);
        
        // 最終スコア計算
        const scores = {
            love: Math.round((baseScores.love * genderModifier * personalModifier * periodModifier) * (todayCompatibility / 100)),
            money: Math.round((baseScores.money * genderModifier * personalModifier * periodModifier) * (todayCompatibility / 100)),
            health: Math.round((baseScores.health * genderModifier * personalModifier * periodModifier) * (todayCompatibility / 100)),
            work: Math.round((baseScores.work * genderModifier * personalModifier * periodModifier) * (todayCompatibility / 100))
        };
        
        scores.overall = Math.round((scores.love + scores.money + scores.health + scores.work) / 4);
        
        // その他の詳細情報
        const personality = this.generatePersonalityAnalysis(fourPillars);
        const recommendations = this.generateDetailedRecommendations(fourPillars, todayData, scores);
        const warnings = this.generateDetailedWarnings(fourPillars, daiun, ryunen);
        const lifeAdvice = this.generateLifeAdvice(fourPillars, daiun);
        
        return {
            fourPillars,
            scores,
            todayCompatibility,
            daiun,
            ryunen,
            personality,
            recommendations,
            warnings,
            lifeAdvice
        };
    }

    /**
     * ユーティリティメソッド群
     */
    getElementFromKan(kan) {
        const elements = {
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火',
            '戊': '土', '己': '土',
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        };
        return elements[kan] || '土';
    }

    getYinYangFromKan(kan) {
        const yangKan = ['甲', '丙', '戊', '庚', '壬'];
        return yangKan.includes(kan) ? '陽' : '陰';
    }

    getAnimalFromShi(shi) {
        const animals = {
            '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兎',
            '辰': '龍', '巳': '蛇', '午': '馬', '未': '羊',
            '申': '猿', '酉': '鶏', '戌': '犬', '亥': '猪'
        };
        return animals[shi] || '龍';
    }

    getYearKanshi(year) {
        const kan = ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'];
        const shi = ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'];
        return kan[year % 10] + shi[year % 12];
    }

    getMonthKanshi(year, month) {
        const monthShi = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        
        const yearKanIndex = year % 10;
        const monthKanIndex = (yearKanIndex * 2 + month - 1) % 10;
        
        return kan[monthKanIndex] + monthShi[(month - 1) % 12];
    }

    getDayKanshi(date) {
        // 簡易計算（実際は複雑な暦計算が必要）
        const baseDate = new Date(1900, 0, 1);
        const daysDiff = Math.floor((date - baseDate) / (1000 * 60 * 60 * 24));
        
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        return kan[daysDiff % 10] + shi[daysDiff % 12];
    }

    isCompatibleElements(element1, element2) {
        const compatible = {
            '木': ['火', '水'],
            '火': ['土', '木'],
            '土': ['金', '火'],
            '金': ['水', '土'],
            '水': ['木', '金']
        };
        return compatible[element1]?.includes(element2) || false;
    }

    isConflictingElements(element1, element2) {
        const conflicting = {
            '木': ['金', '土'],
            '火': ['水', '金'],
            '土': ['木', '水'],
            '金': ['火', '木'],
            '水': ['火', '土']
        };
        return conflicting[element1]?.includes(element2) || false;
    }

    getTodayElement(todayData) {
        // 今日の要素を決定（簡易版）
        const elements = ['木', '火', '土', '金', '水'];
        return elements[todayData.day % 5];
    }

    calculateBaseScores(dayData) {
        return {
            love: 50 + Math.floor(Math.random() * 30),
            money: 50 + Math.floor(Math.random() * 30),
            health: 50 + Math.floor(Math.random() * 30),
            work: 50 + Math.floor(Math.random() * 30)
        };
    }

    calculatePersonalModifier(dayData, fourPillars) {
        const dayElement = fourPillars.day.element;
        let modifier = 1.0;
        
        // 五行による個人修正
        switch (dayElement) {
            case '木': modifier = 1.05; break;
            case '火': modifier = 1.03; break;
            case '土': modifier = 1.00; break;
            case '金': modifier = 0.98; break;
            case '水': modifier = 1.02; break;
        }
        
        return modifier;
    }

    calculateDaiunStartAge(monthPillar, gender) {
        // 簡易計算
        return gender === 'male' ? 8 : 7;
    }

    getDaiunDescription(period, dayElement) {
        const descriptions = {
            0: '運勢上昇期・新しいチャレンジに最適',
            1: '安定期・着実な成長を重視',
            2: '変化期・柔軟な対応が重要',
            3: '発展期・大きな飛躍の可能性',
            4: '調整期・内面の充実を図る',
            5: '成熟期・経験を活かす時'
        };
        return descriptions[period] || '新たな段階への準備期';
    }

    analyzeElementRelationship(dayElement, yearElement) {
        if (this.isCompatibleElements(dayElement, yearElement)) {
            return '相生関係・運気上昇';
        } else if (this.isConflictingElements(dayElement, yearElement)) {
            return '相克関係・注意が必要';
        } else {
            return '中性関係・安定した年';
        }
    }

    calculateRyunenFortune(relationship) {
        const fortunes = {
            '相生関係・運気上昇': { score: 75, description: '良好な運勢' },
            '相克関係・注意が必要': { score: 40, description: '慎重な行動を' },
            '中性関係・安定した年': { score: 60, description: '安定した運勢' }
        };
        return fortunes[relationship] || { score: 50, description: '普通の運勢' };
    }

    calculatePeriodModifier(daiun, ryunen) {
        const daiunModifier = daiun.period < 3 ? 1.05 : 0.95;
        const ryunenModifier = ryunen.fortune.score > 60 ? 1.1 : 0.9;
        return daiunModifier * ryunenModifier;
    }

    generatePersonalityAnalysis(fourPillars) {
        const dayElement = fourPillars.day.element;
        const dayYinYang = fourPillars.day.yinYang;
        
        const personalities = {
            '木': '成長力に富み、創造性豊かな性格です。',
            '火': '情熱的で明るく、リーダーシップを発揮します。',
            '土': '安定感があり、信頼される人格者です。',
            '金': '意志が強く、正義感に満ちた性格です。',
            '水': '柔軟性があり、深い洞察力を持ちます。'
        };
        
        return personalities[dayElement] || 'バランスの取れた性格です。';
    }

    generateDetailedRecommendations(fourPillars, todayData, scores) {
        const recommendations = [];
        const dayElement = fourPillars.day.element;
        
        // 五行別の基本推奨事項
        const elementAdvice = this.getElementSpecificAdvice(dayElement, todayData);
        recommendations.push(...elementAdvice);
        
        // スコアに基づく推奨事項
        if (scores.love < 60) {
            recommendations.push('恋愛運向上のため、今日は' + todayData.color_of_the_day + 'の小物を身につけてみてください。');
        }
        
        if (scores.work < 60) {
            recommendations.push('仕事運を高めるため、' + todayData.meditation_theme + 'を実践してみましょう。');
        }
        
        return recommendations;
    }

    generateDetailedWarnings(fourPillars, daiun, ryunen) {
        const warnings = [];
        
        if (ryunen.fortune.score < 50) {
            warnings.push(ryunen.year + '年は' + ryunen.relationship + 'の年です。慎重な行動を心がけてください。');
        }
        
        if (daiun.period > 3) {
            warnings.push('現在の大運期は変化の時期です。無理をせず体調管理に注意してください。');
        }
        
        return warnings;
    }

    generateLifeAdvice(fourPillars, daiun) {
        const dayElement = fourPillars.day.element;
        return this.getElementLifeAdvice(dayElement);
    }

    getElementSpecificAdvice(element, todayData) {
        const advice = [];
        
        switch (element) {
            case '木':
                advice.push('成長と発展を意識した行動を心がけましょう。');
                advice.push('新しい学びや挑戦が運気を高めます。');
                break;
            case '火':
                advice.push('積極的なコミュニケーションが幸運を呼びます。');
                advice.push('創造的な活動に時間を割いてみてください。');
                break;
            case '土':
                advice.push('基盤を固める活動が今日の開運行動です。');
                advice.push('家族や親しい人との時間を大切にしましょう。');
                break;
            case '金':
                advice.push('規律正しい行動が運気を安定させます。');
                advice.push('美意識と完璧主義を適度に保ち、柔軟性も身につけることが大切です。');
                break;
            case '水':
                advice.push('知恵と直感力を活かし、深い洞察で物事の本質を見抜きましょう。');
                advice.push('流動性を保ちながらも、自分の芯となる価値観を持ち続けてください。');
                break;
        }
        
        return advice;
    }

    getElementLifeAdvice(element) {
        const advice = [];
        
        switch (element) {
            case '木':
                advice.push('常に成長を心がけ、新しいことに挑戦し続けることが人生の鍵です。');
                advice.push('自然との調和を大切にし、環境に配慮した生活を送りましょう。');
                break;
            case '火':
                advice.push('情熱を持って生きることで、周囲の人々を照らす存在になれます。');
                advice.push('創造性を発揮できる分野で才能を開花させましょう。');
                break;
            case '土':
                advice.push('安定した基盤を築くことで、長期的な成功を手にできます。');
                advice.push('人との信頼関係を大切にし、コミュニティに貢献することが重要です。');
                break;
            case '金':
                advice.push('正義感と責任感を持って行動することで、人生の目標を達成できます。');
                advice.push('美意識と完璧主義を適度に保ち、柔軟性も身につけることが大切です。');
                break;
            case '水':
                advice.push('知恵と直感力を活かし、深い洞察で物事の本質を見抜きましょう。');
                advice.push('流動性を保ちながらも、自分の芯となる価値観を持ち続けてください。');
                break;
        }
        
        return advice;
    }
}

// グローバルインスタンス
const detailedFortuneAPI = new DetailedFortuneAPI();