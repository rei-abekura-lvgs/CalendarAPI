/**
 * 暦データAPI 検索機能
 * クライアントサイド検索とフィルタリング
 */

class CalendarSearchAPI {
    constructor() {
        this.dataCache = new Map();
        this.searchHistory = [];
    }

    /**
     * 年間データを取得・キャッシュ
     */
    async loadYearData(year) {
        if (this.dataCache.has(year)) {
            return this.dataCache.get(year);
        }

        try {
            const response = await fetch(`api/${year}/all.json`);
            if (!response.ok) throw new Error(`Failed to load ${year} data`);
            
            const data = await response.json();
            this.dataCache.set(year, data);
            return data;
        } catch (error) {
            console.error(`Error loading ${year} data:`, error);
            return null;
        }
    }

    /**
     * 六曜で検索
     */
    async searchByRokuyo(rokuyo, year = 2025) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        
        // データ構造に応じて処理
        if (data.months && Array.isArray(data.months)) {
            // 階層構造（2026年以降）
            for (const month of data.months) {
                if (month.days) {
                    for (const day of month.days) {
                        if (day.rokuyo === rokuyo) {
                            results.push(day);
                        }
                    }
                }
            }
        } else {
            // フラット構造（2025年）
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && dayData.rokuyo === rokuyo) {
                    results.push({...dayData, date: dateStr});
                }
            }
        }

        this.addToHistory('rokuyo', rokuyo, results.length);
        return results;
    }

    /**
     * 祝日で検索
     */
    async searchHolidays(year = 2025, monthFilter = null) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        
        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (monthFilter && month.month !== monthFilter) continue;
                
                if (month.days) {
                    for (const day of month.days) {
                        if (day.is_holiday && day.holiday_name) {
                            results.push({
                                date: day.date,
                                name: day.holiday_name,
                                month: month.month,
                                weekday: day.weekday
                            });
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && dayData.is_holiday && dayData.holiday_name) {
                    const [y, m, d] = dateStr.split('-').map(Number);
                    if (!monthFilter || m === monthFilter) {
                        results.push({
                            date: dateStr,
                            name: dayData.holiday_name,
                            month: m,
                            weekday: dayData.weekday
                        });
                    }
                }
            }
        }

        this.addToHistory('holidays', `${year}年${monthFilter ? monthFilter + '月' : ''}`, results.length);
        return results;
    }

    /**
     * キーワード検索
     */
    async searchByKeyword(keyword, year = 2025) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        const searchTerm = keyword.toLowerCase();
        
        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (month.days) {
                    for (const day of month.days) {
                        if (this.matchesKeyword(day, searchTerm)) {
                            results.push(day);
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && this.matchesKeyword(dayData, searchTerm)) {
                    results.push({...dayData, date: dateStr});
                }
            }
        }

        this.addToHistory('keyword', keyword, results.length);
        return results;
    }

    /**
     * パワーストーン検索
     */
    async searchByPowerStone(stone, year = 2025) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        
        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (month.days) {
                    for (const day of month.days) {
                        if (day.power_stone && day.power_stone.includes(stone)) {
                            results.push(day);
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && dayData.power_stone && dayData.power_stone.includes(stone)) {
                    results.push({...dayData, date: dateStr});
                }
            }
        }

        this.addToHistory('powerstone', stone, results.length);
        return results;
    }

    /**
     * 週末・平日フィルタ
     */
    async searchWeekends(year = 2025, includeHolidays = true) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        
        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (month.days) {
                    for (const day of month.days) {
                        if (day.is_weekend || (includeHolidays && day.is_holiday)) {
                            results.push(day);
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && 
                    (dayData.is_weekend || (includeHolidays && dayData.is_holiday))) {
                    results.push({...dayData, date: dateStr});
                }
            }
        }

        this.addToHistory('weekends', `${year}年`, results.length);
        return results;
    }

    /**
     * 期間検索
     */
    async searchDateRange(startDate, endDate, year = 2025) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (month.days) {
                    for (const day of month.days) {
                        const dayDate = new Date(day.date);
                        if (dayDate >= start && dayDate <= end) {
                            results.push(day);
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
                    const dayDate = new Date(dateStr);
                    if (dayDate >= start && dayDate <= end) {
                        results.push({...dayData, date: dateStr});
                    }
                }
            }
        }

        this.addToHistory('range', `${startDate} - ${endDate}`, results.length);
        return results;
    }

    /**
     * 一粒万倍日検索
     */
    async searchIchiryuManbaiDays(year = 2025, month = null) {
        const data = await this.loadYearData(year);
        if (!data) return [];

        const results = [];
        
        if (data.months) {
            for (const monthData of data.months) {
                if (month && monthData.month !== month) continue;
                
                if (monthData.days) {
                    for (const day of monthData.days) {
                        if (day.is_ichiryu_manbai) {
                            results.push({
                                date: day.date,
                                day: day.day,
                                month: monthData.month,
                                weekday: day.weekday,
                                rokuyo: day.rokuyo,
                                keyword: day.daily_keyword,
                                isHoliday: day.is_holiday
                            });
                        }
                    }
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/) && dayData.is_ichiryu_manbai) {
                    const [y, m, d] = dateStr.split('-').map(Number);
                    if (!month || m === month) {
                        results.push({
                            date: dateStr,
                            day: d,
                            month: m,
                            weekday: dayData.weekday,
                            rokuyo: dayData.rokuyo,
                            keyword: dayData.daily_keyword,
                            isHoliday: dayData.is_holiday
                        });
                    }
                }
            }
        }

        this.addToHistory('ichiryu_manbai', `${year}年${month ? month + '月' : ''}`, results.length);
        return results;
    }

    /**
     * ラッキーデー検索（大安 + パワーストーン組み合わせ）
     */
    async findLuckyDays(year = 2025, month = null) {
        const rokuyoResults = await this.searchByRokuyo('大安', year);
        
        // 大安の日の中でも特に良いパワーストーンの日を抽出
        const luckyStones = ['水晶', 'アメジスト', 'ローズクォーツ', 'シトリン'];
        
        const luckyDays = rokuyoResults.filter(day => {
            return day.power_stone && luckyStones.some(stone => 
                day.power_stone.includes(stone)
            );
        });

        if (month) {
            return luckyDays.filter(day => {
                const dayMonth = new Date(day.date).getMonth() + 1;
                return dayMonth === month;
            });
        }

        return luckyDays;
    }

    /**
     * キーワードマッチング判定
     */
    matchesKeyword(dayData, searchTerm) {
        const searchableFields = [
            'daily_keyword', 'color_of_the_day', 'recommended_tea',
            'power_stone', 'aroma_oil', 'meditation_theme',
            'flower_language', 'energy_advice', 'astrology_advice',
            'tarot_card', 'wise_saying', 'crystal_healing'
        ];

        return searchableFields.some(field => {
            const value = dayData[field];
            return value && value.toString().toLowerCase().includes(searchTerm);
        });
    }

    /**
     * 検索履歴に追加
     */
    addToHistory(type, query, resultCount) {
        this.searchHistory.unshift({
            type,
            query,
            resultCount,
            timestamp: new Date()
        });

        // 履歴は最新50件まで保持
        if (this.searchHistory.length > 50) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }
    }

    /**
     * 検索履歴取得
     */
    getSearchHistory() {
        return this.searchHistory;
    }

    /**
     * 統計情報取得
     */
    async getStatistics(year = 2025) {
        const data = await this.loadYearData(year);
        if (!data) return null;

        const stats = {
            totalDays: 0,
            holidays: 0,
            weekends: 0,
            rokuyoCount: {},
            powerStoneCount: {},
            colorCount: {}
        };

        const processDay = (dayData) => {
            stats.totalDays++;
            
            if (dayData.is_holiday) stats.holidays++;
            if (dayData.is_weekend) stats.weekends++;
            
            // 六曜統計
            if (dayData.rokuyo) {
                stats.rokuyoCount[dayData.rokuyo] = (stats.rokuyoCount[dayData.rokuyo] || 0) + 1;
            }
            
            // パワーストーン統計
            if (dayData.power_stone) {
                stats.powerStoneCount[dayData.power_stone] = (stats.powerStoneCount[dayData.power_stone] || 0) + 1;
            }
            
            // 色統計
            if (dayData.color_of_the_day) {
                stats.colorCount[dayData.color_of_the_day] = (stats.colorCount[dayData.color_of_the_day] || 0) + 1;
            }
        };

        if (data.months && Array.isArray(data.months)) {
            for (const month of data.months) {
                if (month.days) {
                    month.days.forEach(processDay);
                }
            }
        } else {
            for (const [dateStr, dayData] of Object.entries(data)) {
                if (dateStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
                    processDay(dayData);
                }
            }
        }

        return stats;
    }
}

// グローバルインスタンス
window.calendarSearch = new CalendarSearchAPI();