/**
 * 個人運勢計算API
 * 生年月日を使った個人空亡・運勢計算
 */

class PersonalFortuneAPI {
    constructor() {
        this.birthCache = new Map();
        this.personalCache = new Map();
    }

    /**
     * 生年月日から個人運勢を計算
     */
    async getPersonalFortune(birthDate, targetDate = null) {
        const target = targetDate || new Date();
        const targetStr = this.formatDate(target);
        const cacheKey = `${birthDate}_${targetStr}`;

        if (this.personalCache.has(cacheKey)) {
            return this.personalCache.get(cacheKey);
        }

        try {
            // 日運勢データを取得
            const dayFortune = await this.getDayFortuneData(targetStr);
            if (!dayFortune) throw new Error('日運勢データ取得失敗');

            // 個人空亡計算
            const personalKuubou = this.calculatePersonalKuubou(birthDate, target);
            
            // 生年月日の四柱推命データ
            const birthData = this.calculateBirthData(birthDate);
            
            // 総合運勢計算
            const personalFortune = this.calculatePersonalFortune(
                dayFortune, 
                personalKuubou, 
                birthData
            );

            this.personalCache.set(cacheKey, personalFortune);
            return personalFortune;

        } catch (error) {
            console.error('個人運勢計算エラー:', error);
            return null;
        }
    }

    /**
     * 日運勢データ取得（既存APIから）
     */
    async getDayFortuneData(dateStr) {
        try {
            const [year, month] = dateStr.split('-');
            const response = await fetch(`api/${year}/${month.padStart(2, '0')}.json`);
            
            if (!response.ok) throw new Error(`データ取得失敗: ${dateStr}`);
            
            const monthData = await response.json();
            return monthData.days.find(day => day.date === dateStr);
        } catch (error) {
            console.error('日運勢データ取得エラー:', error);
            return null;
        }
    }

    /**
     * 個人空亡（天中殺）計算
     * 生年で決まる2年間の空亡期間
     */
    calculatePersonalKuubou(birthDate, targetDate) {
        const birth = new Date(birthDate);
        const target = new Date(targetDate);
        
        // 生年の干支を計算
        const birthYear = birth.getFullYear();
        const birthYearKanshi = this.getYearKanshi(birthYear);
        
        // 個人空亡の2年間を計算
        const kuubouYears = this.getPersonalKuubouYears(birthYearKanshi);
        
        // 対象年が空亡年かチェック
        const targetYear = target.getFullYear();
        const isPersonalKuubouYear = kuubouYears.some(year => 
            (targetYear % 12) === (year % 12)
        );

        return {
            isPersonalKuubou: isPersonalKuubouYear,
            kuubouYears: kuubouYears,
            birthYearKanshi: birthYearKanshi,
            nextKuubouStart: this.getNextKuubouYear(targetYear, kuubouYears),
            explanation: this.getPersonalKuubouExplanation(birthYearKanshi)
        };
    }

    /**
     * 年の干支計算（簡易版）
     */
    getYearKanshi(year) {
        // 1984年が甲子（0）として計算
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
            index: kanshiIndex
        };
    }

    /**
     * 個人空亡年計算
     */
    getPersonalKuubouYears(birthYearKanshi) {
        // 十二支ごとの空亡パターン
        const kuubouPattern = {
            '子': [10, 11], // 戌亥年が空亡
            '丑': [10, 11],
            '寅': [0, 1],   // 子丑年が空亡
            '卯': [0, 1],
            '辰': [2, 3],   // 寅卯年が空亡
            '巳': [2, 3],
            '午': [4, 5],   // 辰巳年が空亡
            '未': [4, 5],
            '申': [6, 7],   // 午未年が空亡
            '酉': [6, 7],
            '戌': [8, 9],   // 申酉年が空亡
            '亥': [8, 9]
        };

        return kuubouPattern[birthYearKanshi.shi] || [];
    }

    /**
     * 次の空亡年計算
     */
    getNextKuubouYear(currentYear, kuubouYears) {
        for (let i = 0; i < 12; i++) {
            const checkYear = currentYear + i;
            if (kuubouYears.some(year => (checkYear % 12) === year)) {
                return checkYear;
            }
        }
        return null;
    }

    /**
     * 個人空亡説明文
     */
    getPersonalKuubouExplanation(birthYearKanshi) {
        const explanations = {
            '子': '戌亥年が個人空亡。家庭・不動産・目に見えるものへの影響が大きい時期。',
            '丑': '戌亥年が個人空亡。家庭・不動産・目に見えるものへの影響が大きい時期。',
            '寅': '子丑年が個人空亡。精神世界・学問・宗教への影響が大きい時期。',
            '卯': '子丑年が個人空亡。精神世界・学問・宗教への影響が大きい時期。',
            '辰': '寅卯年が個人空亡。兄弟・友人・東方への影響が大きい時期。',
            '巳': '寅卯年が個人空亡。兄弟・友人・東方への影響が大きい時期。',
            '午': '辰巳年が個人空亡。社会・財運・東南方への影響が大きい時期。',
            '未': '辰巳年が個人空亡。社会・財運・東南方への影響が大きい時期。',
            '申': '午未年が個人空亡。配偶者・恋愛・南方への影響が大きい時期。',
            '酉': '午未年が個人空亡。配偶者・恋愛・南方への影響が大きい時期。',
            '戌': '申酉年が個人空亡。友人・兄弟・西方への影響が大きい時期。',
            '亥': '申酉年が個人空亡。友人・兄弟・西方への影響が大きい時期。'
        };

        return explanations[birthYearKanshi.shi] || '空亡計算中...';
    }

    /**
     * 生年月日の四柱推命データ計算
     */
    calculateBirthData(birthDate) {
        const birth = new Date(birthDate);
        
        // 生年干支
        const yearKanshi = this.getYearKanshi(birth.getFullYear());
        
        // 生月干支（簡易計算）
        const monthIndex = birth.getMonth();
        const monthKanshi = this.getMonthKanshi(birth.getFullYear(), monthIndex);
        
        // 生日干支（1900年1月1日基準）
        const dayKanshi = this.getDayKanshi(birth);

        return {
            year: yearKanshi,
            month: monthKanshi,
            day: dayKanshi,
            personality: this.getPersonalityTraits(yearKanshi, dayKanshi),
            lifeStage: this.getLifeStage(birth)
        };
    }

    /**
     * 月干支計算（簡易版）
     */
    getMonthKanshi(year, monthIndex) {
        const kan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const shi = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑'];
        
        // 年の天干によって月の起点が変わる（簡易計算）
        const yearKan = this.getYearKanshi(year).kan;
        const yearKanIndex = kan.indexOf(yearKan);
        
        const monthKanIndex = (yearKanIndex * 2 + monthIndex + 2) % 10;
        const monthShi = shi[monthIndex];
        
        return {
            kanshi: kan[monthKanIndex] + monthShi,
            kan: kan[monthKanIndex],
            shi: monthShi
        };
    }

    /**
     * 日干支計算
     */
    getDayKanshi(date) {
        // 1900年1月1日を甲子（0）とする
        const baseDate = new Date(1900, 0, 1);
        const diffTime = date.getTime() - baseDate.getTime();
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
            index: kanshiIndex
        };
    }

    /**
     * 性格特性分析
     */
    getPersonalityTraits(yearKanshi, dayKanshi) {
        const traits = {
            strength: this.getStrengthFromKanshi(dayKanshi.kan),
            weakness: this.getWeaknessFromKanshi(dayKanshi.kan),
            element: this.getElementFromKan(dayKanshi.kan),
            animal: this.getAnimalFromShi(yearKanshi.shi)
        };

        return traits;
    }

    /**
     * 人生段階分析
     */
    getLifeStage(birthDate) {
        const now = new Date();
        const age = now.getFullYear() - birthDate.getFullYear();
        
        if (age < 30) return { stage: '青年期', description: '成長と学習の時期' };
        if (age < 50) return { stage: '壮年期', description: '活動と発展の時期' };
        if (age < 70) return { stage: '熟年期', description: '安定と指導の時期' };
        return { stage: '老年期', description: '智慧と伝承の時期' };
    }

    /**
     * 個人運勢総合計算
     */
    calculatePersonalFortune(dayFortune, personalKuubou, birthData) {
        // 基本運勢（日運勢）
        const baseScores = this.calculateBaseScores(dayFortune);
        
        // 個人空亡による修正
        const kuubouModifier = personalKuubou.isPersonalKuubou ? -15 : 0;
        
        // 生年月日による修正
        const personalModifier = this.calculatePersonalModifier(dayFortune, birthData);

        // 最終スコア計算
        const finalScores = {
            love: Math.max(0, Math.min(100, baseScores.love + kuubouModifier + personalModifier.love)),
            money: Math.max(0, Math.min(100, baseScores.money + kuubouModifier + personalModifier.money)),
            health: Math.max(0, Math.min(100, baseScores.health + kuubouModifier + personalModifier.health)),
            work: Math.max(0, Math.min(100, baseScores.work + kuubouModifier + personalModifier.work))
        };

        finalScores.overall = Math.round((finalScores.love + finalScores.money + finalScores.health + finalScores.work) / 4);

        return {
            date: dayFortune.date,
            personalKuubou: personalKuubou,
            birthData: birthData,
            scores: finalScores,
            personalAdvice: this.generatePersonalAdvice(dayFortune, personalKuubou, birthData),
            warnings: this.generatePersonalWarnings(personalKuubou),
            recommendations: this.generatePersonalRecommendations(dayFortune, birthData)
        };
    }

    /**
     * 基本スコア計算（既存ロジック簡易版）
     */
    calculateBaseScores(dayData) {
        let love = 50, money = 50, health = 50, work = 50;

        // 六曜による基本修正
        const rokuyoBonus = {
            '大安': 20, '友引': 15, '先勝': 10,
            '先負': -5, '赤口': -10, '仏滅': -15
        };
        const bonus = rokuyoBonus[dayData.rokuyo] || 0;
        
        love += bonus;
        money += bonus;
        health += bonus;
        work += bonus;

        // 空亡（日）による修正
        if (dayData.is_kuubou) {
            love -= 10;
            money -= 10;
            health -= 5;
            work -= 10;
        }

        return { love, money, health, work };
    }

    /**
     * 個人修正値計算
     */
    calculatePersonalModifier(dayData, birthData) {
        const modifier = { love: 0, money: 0, health: 0, work: 0 };

        // 五行相性チェック
        const dayElement = this.getElementFromKan(dayData.jikkan);
        const birthElement = birthData.day.kan;
        
        if (this.isCompatibleElement(dayElement, birthElement)) {
            modifier.love += 10;
            modifier.work += 10;
        }

        // 十二支相性チェック
        if (this.isCompatibleAnimal(dayData.junishi, birthData.year.shi)) {
            modifier.love += 5;
            modifier.money += 5;
        }

        return modifier;
    }

    /**
     * 個人アドバイス生成
     */
    generatePersonalAdvice(dayData, personalKuubou, birthData) {
        const advice = [];

        if (personalKuubou.isPersonalKuubou) {
            advice.push('個人空亡期間中です。大きな決断は避け、内面を見つめる時期として活用しましょう。');
        }

        advice.push(`あなたの生年干支（${birthData.year.kanshi}）と今日の相性は良好です。`);
        advice.push(`${birthData.personality.element}の性質を活かして、${dayData.daily_keyword}を意識してみてください。`);

        return advice;
    }

    /**
     * 個人警告生成
     */
    generatePersonalWarnings(personalKuubou) {
        const warnings = [];

        if (personalKuubou.isPersonalKuubou) {
            warnings.push('個人空亡期間：転職、結婚、引越しなど人生の重要な決断は慎重に。');
            warnings.push(personalKuubou.explanation);
        }

        return warnings;
    }

    /**
     * 個人推奨事項生成
     */
    generatePersonalRecommendations(dayData, birthData) {
        const recommendations = [];

        recommendations.push(`${birthData.personality.element}属性に合う${dayData.power_stone}を身につけてみてください。`);
        recommendations.push(`${birthData.lifeStage.stage}の特性を活かし、${dayData.meditation_theme}を実践してみましょう。`);

        return recommendations;
    }

    /**
     * ユーティリティメソッド
     */
    getElementFromKan(kan) {
        const elements = {
            '甲': '木', '乙': '木', '丙': '火', '丁': '火',
            '戊': '土', '己': '土', '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        };
        return elements[kan] || '不明';
    }

    getStrengthFromKanshi(kan) {
        const strengths = {
            '甲': '指導力', '乙': '柔軟性', '丙': '情熱', '丁': '繊細さ',
            '戊': '安定性', '己': '包容力', '庚': '意志力', '辛': '美意識',
            '壬': '流動性', '癸': '直感力'
        };
        return strengths[kan] || '調和';
    }

    getWeaknessFromKanshi(kan) {
        const weaknesses = {
            '甲': '頑固さ', '乙': '優柔不断', '丙': '短気', '丁': '神経質',
            '戊': '変化への抵抗', '己': '心配性', '庚': '攻撃性', '辛': '完璧主義',
            '壬': '不安定さ', '癸': '内向性'
        };
        return weaknesses[kan] || '特になし';
    }

    getAnimalFromShi(shi) {
        const animals = {
            '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兎',
            '辰': '龍', '巳': '蛇', '午': '馬', '未': '羊',
            '申': '猿', '酉': '鶏', '戌': '犬', '亥': '猪'
        };
        return animals[shi] || '不明';
    }

    isCompatibleElement(element1, element2) {
        // 簡易五行相性判定
        const compatible = {
            '木': ['水', '木'], '火': ['木', '火'],
            '土': ['火', '土'], '金': ['土', '金'], '水': ['金', '水']
        };
        return compatible[element1]?.includes(element2) || false;
    }

    isCompatibleAnimal(animal1, animal2) {
        // 簡易十二支相性判定（三合・六合）
        const compatible = [
            ['子', '辰', '申'], ['丑', '巳', '酉'], ['寅', '午', '戌'], ['卯', '未', '亥']
        ];
        return compatible.some(group => group.includes(animal1) && group.includes(animal2));
    }

    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
}

// グローバルインスタンス
const personalFortuneAPI = new PersonalFortuneAPI();