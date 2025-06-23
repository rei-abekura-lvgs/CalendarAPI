/**
 * 詳細四柱推命運勢診断API
 * 生年月日時間・性別を使った本格的な運勢計算
 */

class DetailedFortuneAPI {
    constructor() {
        this.detailedCache = new Map();
        this.initializeDateSelectors();
    }

    /**
     * 年月日時間選択肢の初期化
     */
    initializeDateSelectors() {
        // 年選択肢（1940年〜2010年）
        const yearSelect = document.getElementById('birthYear');
        if (yearSelect) {
            for (let year = 2010; year >= 1940; year--) {
                const option = document.createElement('option');
                option.value = year;
                option.textContent = `${year}年`;
                yearSelect.appendChild(option);
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

        // 時間選択肢（0〜23時）
        const hourSelect = document.getElementById('birthHour');
        if (hourSelect) {
            for (let hour = 0; hour <= 23; hour++) {
                const option = document.createElement('option');
                option.value = hour;
                option.textContent = `${hour}時`;
                hourSelect.appendChild(option);
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
        
        // 既存の日選択肢をクリア
        daySelect.innerHTML = '<option value="">日</option>';
        
        // 新しい日選択肢を追加
        for (let day = 1; day <= daysInMonth; day++) {
            const option = document.createElement('option');
            option.value = day;
            option.textContent = `${day}日`;
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

            this.detailedCache.set(cacheKey, detailedFortune);
            return detailedFortune;

        } catch (error) {
            console.error('詳細運勢計算エラー:', error);
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
        const hour = document.getElementById('birthHour')?.value;
        const minute = document.getElementById('birthMinute')?.value || 0;
        const gender = document.querySelector('input[name="gender"]:checked')?.value;

        return {
            year: parseInt(year),
            month: parseInt(month),
            day: parseInt(day),
            hour: hour === 'unknown' ? null : parseInt(hour),
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
        return `${birthData.year}-${birthData.month}-${birthData.day}-${birthData.hour || 'unknown'}-${birthData.minute}-${birthData.gender}`;
    }

    /**
     * 今日のデータ取得
     */
    async getTodayData() {
        const today = new Date();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        
        try {
            const response = await fetch(`api/2025/${month}.json`);
            if (!response.ok) throw new Error('データ取得失敗');
            
            const monthData = await response.json();
            const todayStr = today.toISOString().split('T')[0];
            
            return monthData.days.find(day => day.date === todayStr);
        } catch (error) {
            console.error('今日のデータ取得エラー:', error);
            return null;
        }
    }

    /**
     * 四柱推命計算（年月日時の四柱）
     */
    calculateFourPillars(birthData) {
        const birthDate = new Date(birthData.year, birthData.month - 1, birthData.day, birthData.hour || 12, birthData.minute);
        
        // 年柱計算
        const yearPillar = this.calculateYearPillar(birthData.year);
        
        // 月柱計算
        const monthPillar = this.calculateMonthPillar(birthData.year, birthData.month);
        
        // 日柱計算
        const dayPillar = this.calculateDayPillar(birthDate);
        
        // 時柱計算
        const hourPillar = this.calculateHourPillar(dayPillar.kan, birthData.hour);

        return {
            year: yearPillar,
            month: monthPillar,
            day: dayPillar,
            hour: hourPillar,
            birthDate: birthDate
        };
    }

    /**
     * 年柱計算
     */
    calculateYearPillar(year) {
        // 1984年を甲子（0）として計算
        const baseYear = 1984;
        const yearDiff = year - baseYear;
        const kanshiIndex = yearDiff % 60;
        
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        const kanIndex = kanshiIndex % 10;
        const shiIndex = kanshiIndex % 12;
        
        return {
            kanshi: kan[kanIndex] + shi[shiIndex],
            kan: kan[kanIndex],
            shi: shi[shiIndex],
            kanIndex: kanIndex,
            shiIndex: shiIndex,
            element: this.getElementFromKan(kan[kanIndex]),
            yinYang: this.getYinYangFromKan(kan[kanIndex]),
            animal: this.getAnimalFromShi(shi[shiIndex])
        };
    }

    /**
     * 月柱計算
     */
    calculateMonthPillar(year, month) {
        // 節入り計算は簡略化（実際には節気で計算）
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shi = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];
        
        // 年の天干によって月の起点が変わる
        const yearKanIndex = this.calculateYearPillar(year).kanIndex;
        const monthKanIndex = (yearKanIndex * 2 + month - 1) % 10;
        const monthShiIndex = (month - 1) % 12;
        
        return {
            kanshi: kan[monthKanIndex] + shi[monthShiIndex],
            kan: kan[monthKanIndex],
            shi: shi[monthShiIndex],
            element: this.getElementFromKan(kan[monthKanIndex]),
            yinYang: this.getYinYangFromKan(kan[monthKanIndex]),
            animal: this.getAnimalFromShi(shi[monthShiIndex])
        };
    }

    /**
     * 日柱計算
     */
    calculateDayPillar(birthDate) {
        // 1900年1月1日を甲子（0）とする
        const baseDate = new Date(1900, 0, 1);
        const diffTime = birthDate.getTime() - baseDate.getTime();
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        const kanshiIndex = diffDays % 60;
        
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        const kanIndex = kanshiIndex % 10;
        const shiIndex = kanshiIndex % 12;
        
        return {
            kanshi: kan[kanIndex] + shi[shiIndex],
            kan: kan[kanIndex],
            shi: shi[shiIndex],
            kanIndex: kanIndex,
            shiIndex: shiIndex,
            element: this.getElementFromKan(kan[kanIndex]),
            yinYang: this.getYinYangFromKan(kan[kanIndex]),
            animal: this.getAnimalFromShi(shi[shiIndex])
        };
    }

    /**
     * 時柱計算
     */
    calculateHourPillar(dayKan, hour) {
        if (hour === null) {
            return {
                kanshi: '時間不明',
                kan: '不明',
                shi: '不明',
                element: '不明',
                yinYang: '不明',
                animal: '不明'
            };
        }

        // 時間から時支を決定
        const timeToShi = [
            '子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'
        ];
        
        // 23-1時:子、1-3時:丑、3-5時:寅...
        let shiIndex;
        if (hour === 23 || hour === 0) shiIndex = 0; // 子
        else shiIndex = Math.floor((hour + 1) / 2);
        
        const shi = timeToShi[shiIndex];
        
        // 日干から時干を計算
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const dayKanIndex = kan.indexOf(dayKan);
        const hourKanIndex = (dayKanIndex * 2 + shiIndex) % 10;
        
        return {
            kanshi: kan[hourKanIndex] + shi,
            kan: kan[hourKanIndex],
            shi: shi,
            element: this.getElementFromKan(kan[hourKanIndex]),
            yinYang: this.getYinYangFromKan(kan[hourKanIndex]),
            animal: this.getAnimalFromShi(shi)
        };
    }

    /**
     * 性別による補正計算
     */
    calculateGenderModifier(gender, fourPillars) {
        const modifier = {
            strength: 0,
            sensitivity: 0,
            leadership: 0,
            intuition: 0
        };

        // 日干の陰陽と性別の相性
        const dayYinYang = fourPillars.day.yinYang;
        
        if ((gender === 'male' && dayYinYang === '陽') || 
            (gender === 'female' && dayYinYang === '陰')) {
            // 性別と日干の陰陽が一致
            modifier.strength += 10;
            modifier.leadership += 5;
        } else {
            // 性別と日干の陰陽が異なる
            modifier.sensitivity += 10;
            modifier.intuition += 5;
        }

        return modifier;
    }

    /**
     * 今日との相性計算
     */
    calculateTodayCompatibility(fourPillars, todayData) {
        let compatibility = 50; // 基本値

        // 日干同士の相性
        const dayElement = fourPillars.day.element;
        const todayElement = this.getElementFromKan(todayData.jikkan);
        
        if (this.isCompatibleElements(dayElement, todayElement)) {
            compatibility += 20;
        } else if (this.isConflictingElements(dayElement, todayElement)) {
            compatibility -= 10;
        }

        // 十二支の相性
        const dayAnimal = fourPillars.day.animal;
        const todayAnimal = this.getAnimalFromShi(todayData.junishi);
        
        if (this.isCompatibleAnimals(dayAnimal, todayAnimal)) {
            compatibility += 15;
        }

        return Math.max(0, Math.min(100, compatibility));
    }

    /**
     * 大運計算（10年運）
     */
    calculateDaiun(fourPillars, gender) {
        const now = new Date();
        const age = now.getFullYear() - fourPillars.birthDate.getFullYear();
        
        // 大運の開始年齢を計算（性別と生月により決定）
        const startAge = this.calculateDaiunStartAge(fourPillars.month, gender);
        
        // 現在の大運期を計算
        const daiunPeriod = Math.floor((age - startAge) / 10);
        
        return {
            period: daiunPeriod,
            startAge: startAge + (daiunPeriod * 10),
            endAge: startAge + ((daiunPeriod + 1) * 10),
            description: this.getDaiunDescription(daiunPeriod, fourPillars.day.element)
        };
    }

    /**
     * 流年計算（年運）
     */
    calculateRyunen(fourPillars, currentYear) {
        const ryunenPillar = this.calculateYearPillar(currentYear);
        const dayElement = fourPillars.day.element;
        
        // 流年と日干の関係を分析
        const relationship = this.analyzeElementRelationship(dayElement, ryunenPillar.element);
        
        return {
            year: currentYear,
            pillar: ryunenPillar,
            relationship: relationship,
            fortune: this.calculateRyunenFortune(relationship)
        };
    }

    /**
     * 総合運勢計算
     */
    calculateComprehensiveFortune(fourPillars, genderModifier, todayCompatibility, daiun, ryunen, todayData) {
        // 基本運勢（日干の強弱から）
        const baseScores = this.calculateBaseScores(fourPillars);
        
        // 今日の相性による修正
        const compatibilityModifier = (todayCompatibility - 50) / 5;
        
        // 大運・流年による修正
        const periodModifier = this.calculatePeriodModifier(daiun, ryunen);

        // 最終スコア計算
        const finalScores = {
            love: Math.max(0, Math.min(100, 
                baseScores.love + compatibilityModifier + periodModifier.love + genderModifier.sensitivity)),
            money: Math.max(0, Math.min(100, 
                baseScores.money + compatibilityModifier + periodModifier.money + genderModifier.strength)),
            health: Math.max(0, Math.min(100, 
                baseScores.health + compatibilityModifier + periodModifier.health)),
            work: Math.max(0, Math.min(100, 
                baseScores.work + compatibilityModifier + periodModifier.work + genderModifier.leadership)),
            overall: 0
        };

        finalScores.overall = Math.round(
            (finalScores.love + finalScores.money + finalScores.health + finalScores.work) / 4
        );

        return {
            date: todayData.date,
            fourPillars: fourPillars,
            genderModifier: genderModifier,
            todayCompatibility: todayCompatibility,
            daiun: daiun,
            ryunen: ryunen,
            scores: finalScores,
            personality: this.generatePersonalityAnalysis(fourPillars),
            recommendations: this.generateDetailedRecommendations(fourPillars, todayData, finalScores),
            warnings: this.generateDetailedWarnings(fourPillars, daiun, ryunen),
            lifeAdvice: this.generateLifeAdvice(fourPillars, daiun)
        };
    }

    /**
     * ユーティリティメソッド群
     */
    getElementFromKan(kan) {
        const elements = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火',
            '戊': '土', '己': '土', '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        };
        return elements[kan] || '不明';
    }

    getYinYangFromKan(kan) {
        const yinYang = {
            '甲': '陽', '乙': '陰', '丙': '陽', '丁': '陰',
            '戊': '陽', '己': '陰', '庚': '陽', '辛': '陰',
            '壬': '陽', '癸': '陰'
        };
        return yinYang[kan] || '不明';
    }

    getAnimalFromShi(shi) {
        const animals = {
            '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兎',
            '辰': '龍', '巳': '蛇', '午': '馬', '未': '羊',
            '申': '猿', '酉': '鶏', '戌': '犬', '亥': '猪'
        };
        return animals[shi] || '不明';
    }

    isCompatibleElements(element1, element2) {
        const compatible = {
            '木': ['水'], '火': ['木'], '土': ['火'], 
            '金': ['土'], '水': ['金']
        };
        return compatible[element1]?.includes(element2) || compatible[element2]?.includes(element1);
    }

    isConflictingElements(element1, element2) {
        const conflicts = {
            '木': ['金'], '火': ['水'], '土': ['木'], 
            '金': ['火'], '水': ['土']
        };
        return conflicts[element1]?.includes(element2) || conflicts[element2]?.includes(element1);
    }

    isCompatibleAnimals(animal1, animal2) {
        const compatible = [
            ['鼠', '龍', '猿'], ['牛', '蛇', '鶏'], 
            ['虎', '馬', '犬'], ['兎', '羊', '猪']
        ];
        return compatible.some(group => group.includes(animal1) && group.includes(animal2));
    }

    calculateBaseScores(fourPillars) {
        // 生年月日による個別スコア計算
        const dayElement = fourPillars.day.element;
        const dayKan = fourPillars.day.kan;
        const birthDate = fourPillars.birthDate;
        
        // 生年月日から基本値を算出（固定値を避ける）
        const dayOfYear = Math.floor((birthDate - new Date(birthDate.getFullYear(), 0, 0)) / 86400000);
        const birthVariation = (dayOfYear % 20) - 10; // -10から+9の範囲
        
        const baseScore = 50 + birthVariation;
        
        return {
            love: baseScore + this.getElementBonus(dayElement, 'love') + this.getKanModifier(dayKan, 'love'),
            money: baseScore + this.getElementBonus(dayElement, 'money') + this.getKanModifier(dayKan, 'money'),
            health: baseScore + this.getElementBonus(dayElement, 'health') + this.getKanModifier(dayKan, 'health'),
            work: baseScore + this.getElementBonus(dayElement, 'work') + this.getKanModifier(dayKan, 'work')
        };
    }

    getElementBonus(element, category) {
        const bonuses = {
            '木': { love: 10, money: 0, health: 5, work: 5 },
            '火': { love: 15, money: 5, health: 0, work: 10 },
            '土': { love: 5, money: 10, health: 10, work: 5 },
            '金': { love: 0, money: 15, health: 5, work: 10 },
            '水': { love: 10, money: 5, health: 10, work: 5 }
        };
        return bonuses[element]?.[category] || 0;
    }

    /**
     * 十干による個別修正値
     */
    getKanModifier(kan, category) {
        const modifiers = {
            '甲': { love: 5, money: -3, health: 2, work: 8 },
            '乙': { love: 8, money: 2, health: 5, work: -2 },
            '丙': { love: 10, money: 3, health: -5, work: 7 },
            '丁': { love: 12, money: -2, health: 3, work: 2 },
            '戊': { love: -2, money: 8, health: 8, work: 3 },
            '己': { love: 3, money: 5, health: 10, work: -3 },
            '庚': { love: -5, money: 12, health: 2, work: 8 },
            '辛': { love: 2, money: 10, health: 3, work: 5 },
            '壬': { love: 7, money: 2, health: 8, work: 3 },
            '癸': { love: 10, money: -2, health: 12, work: -3 }
        };
        return modifiers[kan]?.[category] || 0;
    }

    calculateDaiunStartAge(monthPillar, gender) {
        // 簡略化：性別により基本開始年齢を設定
        return gender === 'male' ? 8 : 7;
    }

    getDaiunDescription(period, dayElement) {
        const descriptions = [
            '青年期 - 学習と成長の時期',
            '青年後期 - 実力蓄積の時期', 
            '壮年期 - 活動と発展の時期',
            '壮年後期 - 責任と指導の時期',
            '熟年期 - 安定と智慧の時期',
            '熟年後期 - 伝承と調和の時期'
        ];
        return descriptions[Math.min(period, descriptions.length - 1)] || '人生後期 - 達観の時期';
    }

    analyzeElementRelationship(dayElement, yearElement) {
        if (dayElement === yearElement) return '比肩・劫財';
        if (this.isCompatibleElements(dayElement, yearElement)) return '印綬・偏印';
        if (this.isConflictingElements(dayElement, yearElement)) return '官殺';
        return '食傷・財星';
    }

    calculateRyunenFortune(relationship) {
        const fortunes = {
            '比肩・劫財': { score: 60, description: '競争と協力の年' },
            '印綬・偏印': { score: 80, description: '学習と成長の年' },
            '官殺': { score: 40, description: '責任と試練の年' },
            '食傷・財星': { score: 70, description: '創造と収穫の年' }
        };
        return fortunes[relationship] || { score: 50, description: '変化の年' };
    }

    calculatePeriodModifier(daiun, ryunen) {
        const daiunBonus = Math.floor(daiun.period / 2) * 2;
        const ryunenBonus = (ryunen.fortune.score - 50) / 10;
        
        return {
            love: daiunBonus + ryunenBonus,
            money: daiunBonus + ryunenBonus,
            health: daiunBonus,
            work: daiunBonus + ryunenBonus
        };
    }

    generatePersonalityAnalysis(fourPillars) {
        const dayElement = fourPillars.day.element;
        const dayYinYang = fourPillars.day.yinYang;
        
        const personalities = {
            '木': {
                '陽': '成長志向で積極的。リーダーシップがあり、新しいことにチャレンジする勇気を持つ。',
                '陰': '柔軟性があり協調性が高い。周囲との調和を大切にし、着実に成長していく。'
            },
            '火': {
                '陽': '情熱的で行動力がある。明るく社交的で、周囲を明るく照らす存在。',
                '陰': '繊細で感受性が豊か。芸術的センスがあり、美しいものを愛する。'
            },
            '土': {
                '陽': '安定感があり信頼される。現実的で着実、責任感が強い。',
                '陰': '包容力があり面倒見が良い。優しく温かい心を持つ。'
            },
            '金': {
                '陽': '意志が強く決断力がある。正義感が強く、筋を通す。',
                '陰': '美意識が高く洗練されている。品格があり、完璧を求める。'
            },
            '水': {
                '陽': '流動性があり適応力が高い。知恵があり、状況に応じて柔軟に対応する。',
                '陰': '直感力が鋭く洞察力がある。静かな中に深い智慧を秘めている。'
            }
        };

        return personalities[dayElement]?.[dayYinYang] || '独特の個性を持つ魅力的な人格。';
    }

    generateDetailedRecommendations(fourPillars, todayData, scores) {
        const recommendations = [];
        
        // 日干に基づく推奨事項
        const dayElement = fourPillars.day.element;
        const elementAdvice = this.getElementSpecificAdvice(dayElement, todayData);
        recommendations.push(...elementAdvice);
        
        // スコアに基づく推奨事項
        if (scores.love < 60) {
            recommendations.push(`恋愛運向上のため、今日は${todayData.color_of_the_day}の小物を身につけてみてください。`);
            recommendations.push(`${todayData.flower_message}の花言葉を意識して、愛情表現を豊かにしましょう。`);
        }
        
        if (scores.work < 60) {
            recommendations.push(`仕事運を高めるため、${todayData.meditation_theme}を実践してみましょう。`);
            recommendations.push(`集中力を高めるため、${todayData.aroma_oil}のアロマを取り入れてください。`);
        }
        
        if (scores.money < 60) {
            recommendations.push(`金運向上のため、${todayData.power_stone}を持ち歩くと良いでしょう。`);
            recommendations.push(`今日のラッキーナンバー${todayData.lucky_number}を意識した行動をとってみてください。`);
        }
        
        if (scores.health < 60) {
            recommendations.push(`健康運のため、${todayData.recommended_tea}を飲んでリラックスしましょう。`);
            recommendations.push(`${todayData.crystal_healing}のエネルギーで心身を整えてください。`);
        }

        return recommendations;
    }

    generateDetailedWarnings(fourPillars, daiun, ryunen) {
        const warnings = [];
        
        if (ryunen.fortune.score < 50) {
            warnings.push(`${ryunen.year}年は${ryunen.relationship}の年です。慎重な行動を心がけてください。`);
        }
        
        if (daiun.period >= 4) {
            warnings.push('人生の転換期です。大きな決断は慎重に検討しましょう。');
        }

        return warnings;
    }

    generateLifeAdvice(fourPillars, daiun) {
        const advice = [];
        
        advice.push(`現在は${daiun.description}です。この時期の特性を活かしていきましょう。`);
        advice.push(`あなたの日干（${fourPillars.day.kan}）は${fourPillars.day.element}属性で${fourPillars.day.yinYang}の性質を持ちます。`);
        
        // 五行に基づく人生アドバイス
        const elementAdvice = this.getElementLifeAdvice(fourPillars.day.element);
        advice.push(...elementAdvice);
        
        return advice;
    }

    /**
     * 五行属性別の具体的アドバイス生成
     */
    getElementSpecificAdvice(element, todayData) {
        const advice = [];
        
        // 五行属性に基づくパワーストーン推奨
        const personalStone = this.getPersonalPowerStone(element);
        
        switch(element) {
            case '木':
                advice.push(`木属性のあなたには、${personalStone}が成長エネルギーを高めます。`);
                advice.push(`創造性を活かす仕事や趣味に力を注ぐと良い日です。`);
                advice.push(`今日は${todayData.meditation_theme}の瞑想で内なる成長を促しましょう。`);
                break;
            case '火':
                advice.push(`火属性のあなたには、${personalStone}で情熱をコントロールしましょう。`);
                advice.push(`人とのコミュニケーションを大切にする日です。`);
                advice.push(`${todayData.aroma_oil}のアロマで感情のバランスを整えてください。`);
                break;
            case '土':
                advice.push(`土属性のあなたには、${personalStone}が安定感をもたらします。`);
                advice.push(`基盤固めや計画立案に適した日です。`);
                advice.push(`${todayData.crystal_healing}のエネルギーで地に足をつけた行動を。`);
                break;
            case '金':
                advice.push(`金属性のあなたには、${personalStone}が決断力を高めます。`);
                advice.push(`整理整頓や品質向上に取り組むと良い日です。`);
                advice.push(`${todayData.feng_shui_advice}を参考に環境を整えましょう。`);
                break;
            case '水':
                advice.push(`水属性のあなたには、${personalStone}で直感力を研ぎ澄ませましょう。`);
                advice.push(`学習や研究、深い思考に適した日です。`);
                advice.push(`${todayData.recommended_tea}を飲んで心を静めてください。`);
                break;
        }
        
        return advice;
    }

    /**
     * 五行属性に基づく個人専用パワーストーン
     */
    getPersonalPowerStone(element) {
        const stones = {
            '木': ['アベンチュリン', 'プレナイト', 'ペリドット', 'グリーンアゲート'],
            '火': ['カーネリアン', 'サンストーン', 'ルビー', 'ガーネット'],
            '土': ['タイガーアイ', 'シトリン', 'イエロージャスパー', 'スモーキークォーツ'],
            '金': ['ローズクォーツ', 'クンツァイト', 'モルガナイト', 'ピンクトルマリン'],
            '水': ['アクアマリン', 'ブルーレースアゲート', 'ソーダライト', 'ラピスラズリ']
        };
        
        const stoneList = stones[element] || ['クリアクォーツ'];
        const index = Math.floor(Math.random() * stoneList.length);
        return stoneList[index];
    }

    /**
     * 五行別の人生アドバイス
     */
    getElementLifeAdvice(element) {
        const advice = [];
        
        switch(element) {
            case '木':
                advice.push('成長と発展を重視し、常に新しい挑戦を恐れないことが大切です。');
                advice.push('協調性を活かしながらも、自分の信念を貫く強さを持ちましょう。');
                break;
            case '火':
                advice.push('情熱と行動力を活かし、周囲を明るく照らす存在になりましょう。');
                advice.push('感情のコントロールを学び、持続可能な情熱を維持することが重要です。');
                break;
            case '土':
                advice.push('安定と信頼を基盤に、着実に目標に向かって進みましょう。');
                advice.push('包容力を活かし、周囲をサポートする役割を大切にしてください。');
                break;
            case '金':
                advice.push('正義感と意志の強さを活かし、筋の通った生き方を貫きましょう。');
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