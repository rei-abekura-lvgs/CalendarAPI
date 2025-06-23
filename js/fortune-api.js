/**
 * 暦データAPI 運勢機能
 * 27項目データを統合した総合運勢表示
 */

class FortuneAPI {
    constructor() {
        this.fortuneCache = new Map();
        this.algorithms = {
            love: this.calculateLoveScore.bind(this),
            money: this.calculateMoneyScore.bind(this),
            health: this.calculateHealthScore.bind(this),
            work: this.calculateWorkScore.bind(this),
            overall: this.calculateOverallScore.bind(this)
        };
    }

    /**
     * 今日の総合運勢を取得
     */
    async getTodaysFortune() {
        const today = new Date();
        const dateStr = this.formatDate(today);
        
        return await this.getDateFortune(dateStr);
    }

    /**
     * 指定日の運勢を取得
     */
    async getDateFortune(dateStr) {
        if (this.fortuneCache.has(dateStr)) {
            return this.fortuneCache.get(dateStr);
        }

        try {
            const [year, month] = dateStr.split('-');
            const response = await fetch(`api/${year}/${month.padStart(2, '0')}.json`);
            
            if (!response.ok) throw new Error(`Failed to load data for ${dateStr}`);
            
            const monthData = await response.json();
            const dayData = this.findDayData(monthData, dateStr);
            
            if (!dayData) throw new Error(`Day data not found for ${dateStr}`);
            
            const fortune = this.calculateFortune(dayData);
            this.fortuneCache.set(dateStr, fortune);
            
            return fortune;
        } catch (error) {
            console.error(`Error getting fortune for ${dateStr}:`, error);
            return null;
        }
    }

    /**
     * 月データから特定日を抽出
     */
    findDayData(monthData, dateStr) {
        if (monthData.days && Array.isArray(monthData.days)) {
            return monthData.days.find(day => day.date === dateStr);
        } else {
            return monthData[dateStr];
        }
    }

    /**
     * 総合運勢計算
     */
    calculateFortune(dayData) {
        const scores = {
            love: this.algorithms.love(dayData),
            money: this.algorithms.money(dayData),
            health: this.algorithms.health(dayData),
            work: this.algorithms.work(dayData)
        };
        
        scores.overall = this.algorithms.overall(dayData, scores);

        return {
            date: dayData.date,
            weekday: dayData.weekday,
            scores: scores,
            recommendations: this.generateRecommendations(dayData, scores),
            warnings: this.generateWarnings(dayData, scores),
            highlights: this.getHighlights(dayData),
            summary: this.generateSummary(dayData, scores),
            rawData: {
                rokuyo: dayData.rokuyo,
                keyword: dayData.daily_keyword,
                color: dayData.color_of_the_day,
                powerStone: dayData.power_stone,
                aromaOil: dayData.aroma_oil,
                tarotCard: dayData.tarot_card
            }
        };
    }

    /**
     * 恋愛運計算
     */
    calculateLoveScore(dayData) {
        let score = 50; // ベース値

        // 六曜による影響
        const rokuyoBonus = {
            '大安': 25, '友引': 15, '先勝': 10,
            '先負': 5, '赤口': -10, '仏滅': -20
        };
        score += rokuyoBonus[dayData.rokuyo] || 0;

        // パワーストーンによる影響
        const loveStones = ['ローズクォーツ', 'ガーネット', 'ムーンストーン', 'エメラルド'];
        if (dayData.power_stone && loveStones.includes(dayData.power_stone)) {
            score += 15;
        }

        // 色による影響
        const loveColors = ['ピンク', '赤色', '桃色', '薔薇色'];
        if (dayData.color_of_the_day && loveColors.some(color => 
            dayData.color_of_the_day.includes(color))) {
            score += 10;
        }

        // タロットカードによる影響
        const loveCards = ['恋人', 'カップ', '女帝', '星'];
        if (dayData.tarot_card && loveCards.some(card => 
            dayData.tarot_card.includes(card))) {
            score += 12;
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * 金運計算
     */
    calculateMoneyScore(dayData) {
        let score = 50;

        const rokuyoBonus = {
            '大安': 20, '友引': 10, '先勝': 15,
            '先負': 5, '赤口': -5, '仏滅': -15
        };
        score += rokuyoBonus[dayData.rokuyo] || 0;

        const moneyStones = ['シトリン', 'タイガーアイ', 'パイライト', '金運石'];
        if (dayData.power_stone && moneyStones.includes(dayData.power_stone)) {
            score += 20;
        }

        const moneyColors = ['金色', '黄色', '緑色', '金運色'];
        if (dayData.color_of_the_day && moneyColors.some(color => 
            dayData.color_of_the_day.includes(color))) {
            score += 10;
        }

        if (dayData.daily_keyword && (
            dayData.daily_keyword.includes('金運') || 
            dayData.daily_keyword.includes('財運') ||
            dayData.daily_keyword.includes('豊かさ'))) {
            score += 15;
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * 健康運計算
     */
    calculateHealthScore(dayData) {
        let score = 50;

        const rokuyoBonus = {
            '大安': 15, '友引': 12, '先勝': 8,
            '先負': 8, '赤口': -8, '仏滅': -12
        };
        score += rokuyoBonus[dayData.rokuyo] || 0;

        const healthStones = ['アメジスト', '水晶', 'フローライト', 'アベンチュリン'];
        if (dayData.power_stone && healthStones.includes(dayData.power_stone)) {
            score += 15;
        }

        if (dayData.meditation_theme) {
            score += 10;
        }

        if (dayData.aroma_oil && (
            dayData.aroma_oil.includes('ラベンダー') ||
            dayData.aroma_oil.includes('ユーカリ') ||
            dayData.aroma_oil.includes('ティーツリー'))) {
            score += 8;
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * 仕事運計算
     */
    calculateWorkScore(dayData) {
        let score = 50;

        const rokuyoBonus = {
            '大安': 20, '先勝': 18, '友引': 10,
            '先負': 5, '赤口': -10, '仏滅': -15
        };
        score += rokuyoBonus[dayData.rokuyo] || 0;

        const workStones = ['タイガーアイ', 'カーネリアン', 'ヘマタイト', 'フローライト'];
        if (dayData.power_stone && workStones.includes(dayData.power_stone)) {
            score += 15;
        }

        if (dayData.daily_keyword && (
            dayData.daily_keyword.includes('成功') || 
            dayData.daily_keyword.includes('達成') ||
            dayData.daily_keyword.includes('前進'))) {
            score += 12;
        }

        if (dayData.is_weekend) {
            score -= 10; // 週末は仕事運下がる
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * 総合運計算
     */
    calculateOverallScore(dayData, scores) {
        const average = (scores.love + scores.money + scores.health + scores.work) / 4;
        
        // 祝日ボーナス
        if (dayData.is_holiday) {
            return Math.min(100, average + 10);
        }

        return average;
    }

    /**
     * おすすめアクション生成
     */
    generateRecommendations(dayData, scores) {
        const recommendations = [];

        // 最も高いスコアに基づく推奨
        const maxScore = Math.max(scores.love, scores.money, scores.health, scores.work);
        
        if (scores.love === maxScore && scores.love >= 70) {
            const colorText = dayData.color_of_the_day || '明るい色';
            const stoneText = dayData.power_stone || 'お気に入りのアクセサリー';
            recommendations.push({
                type: 'love',
                action: '恋愛運が絶好調です。積極的な行動を。',
                detail: `${stoneText}を身につけて、${colorText}を意識したファッションで。`
            });
        }

        if (scores.money === maxScore && scores.money >= 70) {
            const teaText = dayData.recommended_tea || 'お気に入りのお茶';
            recommendations.push({
                type: 'money',
                action: '金運が上昇中。投資や重要な買い物に良い日。',
                detail: `${teaText}を飲んで金運パワーをチャージ。`
            });
        }

        if (scores.health >= 70) {
            const aromaText = dayData.aroma_oil || 'リラックス効果のあるアロマ';
            recommendations.push({
                type: 'health',
                action: '健康運良好。新しい運動習慣を始めるのに最適。',
                detail: `${aromaText}でリラックスタイムを。`
            });
        }

        if (scores.work >= 70) {
            recommendations.push({
                type: 'work',
                action: '仕事運が好調。重要な決断や新プロジェクトの開始に。',
                detail: `${dayData.meditation_theme}で集中力を高めて。`
            });
        }

        // 六曜に基づく推奨
        if (dayData.rokuyo === '大安') {
            recommendations.push({
                type: 'general',
                action: '大安の日。新しいことを始めるのに最適。',
                detail: '契約、結婚、開店など重要な行事に向いています。'
            });
        }

        return recommendations;
    }

    /**
     * 注意事項生成
     */
    generateWarnings(dayData, scores) {
        const warnings = [];

        // 低スコアに基づく警告
        if (scores.love < 30) {
            warnings.push({
                type: 'love',
                message: '恋愛運が低迷中。無理をせず、自分磨きに集中を。'
            });
        }

        if (scores.money < 30) {
            warnings.push({
                type: 'money',
                message: '金運注意。大きな買い物や投資は避けた方が無難。'
            });
        }

        if (dayData.rokuyo === '仏滅') {
            warnings.push({
                type: 'general',
                message: '仏滅の日。新しいことは避け、整理整頓や準備に集中を。'
            });
        }

        if (dayData.rokuyo === '赤口') {
            warnings.push({
                type: 'general',
                message: '赤口の日。口論やトラブルに注意。慎重な行動を。'
            });
        }

        return warnings;
    }

    /**
     * 今日のハイライト
     */
    getHighlights(dayData) {
        return {
            keyword: dayData.daily_keyword,
            color: dayData.color_of_the_day,
            powerStone: dayData.power_stone,
            tea: dayData.recommended_tea,
            aroma: dayData.aroma_oil,
            tarot: dayData.tarot_card,
            advice: dayData.energy_advice
        };
    }

    /**
     * 運勢サマリー生成
     */
    generateSummary(dayData, scores) {
        const avgScore = scores.overall;
        let level, message;

        if (avgScore >= 80) {
            level = '絶好調';
            message = '全体的に非常に良い運勢です。積極的な行動で大きな成果を期待できます。';
        } else if (avgScore >= 60) {
            level = '好調';
            message = '良い流れの日です。計画していたことを実行に移すのに適しています。';
        } else if (avgScore >= 40) {
            level = '普通';
            message = '平穏な一日。現状維持を心がけ、無理のない範囲で過ごしましょう。';
        } else if (avgScore >= 20) {
            level = '注意';
            message = '少し慎重に。急がず焦らず、準備や見直しに時間を使いましょう。';
        } else {
            level = '要注意';
            message = '今日は守りの日。新しいことは避け、リラックスして過ごすのが吉。';
        }

        return {
            level,
            score: Math.round(avgScore),
            message,
            rokuyo: dayData.rokuyo,
            specialNote: this.getSpecialNote(dayData)
        };
    }

    /**
     * 特別メモ生成
     */
    getSpecialNote(dayData) {
        if (dayData.is_holiday) {
            return `${dayData.holiday_name}の特別な日。心も軽やかに過ごしましょう。`;
        }

        if (dayData.rokuyo === '大安') {
            return '大安の日。何事も吉とされる最高の日です。';
        }

        if (dayData.daily_keyword && dayData.daily_keyword.includes('龍神')) {
            return '龍神様のご加護を感じられる神秘的な日。';
        }

        return `${dayData.daily_keyword}がキーワードの日。この言葉を意識して過ごしてみて。`;
    }

    /**
     * 日付フォーマット
     */
    formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    /**
     * 週間運勢取得
     */
    async getWeeklyFortune(startDate = null) {
        const start = startDate ? new Date(startDate) : new Date();
        const fortunes = [];

        for (let i = 0; i < 7; i++) {
            const date = new Date(start);
            date.setDate(start.getDate() + i);
            const dateStr = this.formatDate(date);
            
            try {
                const fortune = await this.getDateFortune(dateStr);
                if (fortune) {
                    fortunes.push(fortune);
                }
            } catch (error) {
                console.error(`Error getting fortune for ${dateStr}:`, error);
            }
        }

        return fortunes;
    }

    /**
     * 相性診断
     */
    async getCompatibility(date1, date2) {
        try {
            const fortune1 = await this.getDateFortune(date1);
            const fortune2 = await this.getDateFortune(date2);

            if (!fortune1 || !fortune2) {
                throw new Error('相性診断用のデータを取得できませんでした');
            }

            const compatibility = this.calculateCompatibility(fortune1, fortune2);
            
            return {
                date1,
                date2,
                compatibility,
                analysis: this.generateCompatibilityAnalysis(fortune1, fortune2, compatibility)
            };
        } catch (error) {
            console.error('Compatibility calculation error:', error);
            return null;
        }
    }

    /**
     * 相性スコア計算
     */
    calculateCompatibility(fortune1, fortune2) {
        let score = 50;

        // 六曜の相性
        const rokuyoCompatibility = {
            '大安': ['大安', '友引', '先勝'],
            '友引': ['大安', '友引', '先負'],
            '先勝': ['大安', '先勝', '赤口'],
            '先負': ['友引', '先負', '仏滅'],
            '赤口': ['先勝', '赤口'],
            '仏滅': ['先負', '仏滅']
        };

        if (rokuyoCompatibility[fortune1.rawData.rokuyo]?.includes(fortune2.rawData.rokuyo)) {
            score += 15;
        }

        // パワーストーンの相性
        if (fortune1.rawData.powerStone === fortune2.rawData.powerStone) {
            score += 20;
        }

        // 色の相性
        if (fortune1.rawData.color === fortune2.rawData.color) {
            score += 10;
        }

        // 運勢スコアの相性
        const scoreDiff = Math.abs(fortune1.scores.overall - fortune2.scores.overall);
        if (scoreDiff < 20) {
            score += 10;
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * 相性分析文生成
     */
    generateCompatibilityAnalysis(fortune1, fortune2, score) {
        let level, message;

        if (score >= 80) {
            level = '最高の相性';
            message = '非常に相性が良い組み合わせです。一緒に過ごすことで互いの運気が上昇します。';
        } else if (score >= 60) {
            level = '良好な相性';
            message = '相性の良い組み合わせ。お互いを高め合える関係性です。';
        } else if (score >= 40) {
            level = '普通の相性';
            message = '平均的な相性。特別な問題はありませんが、理解し合う努力が必要です。';
        } else {
            level = '要注意';
            message = '少し注意が必要な組み合わせ。互いの違いを尊重することが大切です。';
        }

        return {
            level,
            score,
            message,
            details: {
                rokuyoMatch: fortune1.rawData.rokuyo === fortune2.rawData.rokuyo,
                stoneMatch: fortune1.rawData.powerStone === fortune2.rawData.powerStone,
                colorMatch: fortune1.rawData.color === fortune2.rawData.color
            }
        };
    }
}

// グローバルインスタンス
window.fortuneAPI = new FortuneAPI();