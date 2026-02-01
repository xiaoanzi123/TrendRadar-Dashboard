import pg from 'pg';

const { Client } = pg;
const connectionString = 'postgresql://postgres:CAF@sbb1991328@db.sqnfcrywcddssjopdcde.supabase.co:5432/postgres';

const sampleNews = [
  // 微博热搜
  { platform_id: 'weibo', title: '春节档电影票房破纪录', url: 'https://weibo.com/1', rank: 1, hot_value: '4521万' },
  { platform_id: 'weibo', title: 'AI技术新突破引发热议', url: 'https://weibo.com/2', rank: 2, hot_value: '3892万' },
  { platform_id: 'weibo', title: '某明星官宣恋情', url: 'https://weibo.com/3', rank: 3, hot_value: '3654万' },
  { platform_id: 'weibo', title: '新能源汽车降价潮来袭', url: 'https://weibo.com/4', rank: 4, hot_value: '2987万' },
  { platform_id: 'weibo', title: '全国多地迎来降雪', url: 'https://weibo.com/5', rank: 5, hot_value: '2765万' },

  // 知乎热榜
  { platform_id: 'zhihu', title: '如何看待ChatGPT最新更新？', url: 'https://zhihu.com/1', rank: 1, hot_value: '1254万热度' },
  { platform_id: 'zhihu', title: '2026年程序员就业形势分析', url: 'https://zhihu.com/2', rank: 2, hot_value: '987万热度' },
  { platform_id: 'zhihu', title: '为什么越来越多人选择远程工作？', url: 'https://zhihu.com/3', rank: 3, hot_value: '876万热度' },
  { platform_id: 'zhihu', title: '如何评价最新的iPhone？', url: 'https://zhihu.com/4', rank: 4, hot_value: '765万热度' },
  { platform_id: 'zhihu', title: '年轻人该不该买房？', url: 'https://zhihu.com/5', rank: 5, hot_value: '654万热度' },

  // 抖音热榜
  { platform_id: 'douyin', title: '春节特效妆容教程', url: 'https://douyin.com/1', rank: 1, hot_value: '5432万播放' },
  { platform_id: 'douyin', title: '东北雪景vlog', url: 'https://douyin.com/2', rank: 2, hot_value: '4321万播放' },
  { platform_id: 'douyin', title: '年夜饭硬菜教学', url: 'https://douyin.com/3', rank: 3, hot_value: '3987万播放' },
  { platform_id: 'douyin', title: '春节回家搞笑段子', url: 'https://douyin.com/4', rank: 4, hot_value: '3654万播放' },
  { platform_id: 'douyin', title: '新年穿搭分享', url: 'https://douyin.com/5', rank: 5, hot_value: '3210万播放' },

  // B站热门
  { platform_id: 'bilibili', title: '【技术分享】从零搭建个人博客', url: 'https://bilibili.com/1', rank: 1, hot_value: '234万播放' },
  { platform_id: 'bilibili', title: '春节档电影深度解析', url: 'https://bilibili.com/2', rank: 2, hot_value: '198万播放' },
  { platform_id: 'bilibili', title: '游戏《黑神话：悟空》全流程攻略', url: 'https://bilibili.com/3', rank: 3, hot_value: '176万播放' },
  { platform_id: 'bilibili', title: 'AI绘画教程合集', url: 'https://bilibili.com/4', rank: 4, hot_value: '154万播放' },
  { platform_id: 'bilibili', title: '年度科技产品盘点', url: 'https://bilibili.com/5', rank: 5, hot_value: '132万播放' },

  // 百度热搜
  { platform_id: 'baidu', title: '春运火车票抢票攻略', url: 'https://baidu.com/1', rank: 1, hot_value: '4987654' },
  { platform_id: 'baidu', title: '全国天气预报', url: 'https://baidu.com/2', rank: 2, hot_value: '4321098' },
  { platform_id: 'baidu', title: '春节放假安排', url: 'https://baidu.com/3', rank: 3, hot_value: '3876543' },
  { platform_id: 'baidu', title: '新冠疫情最新消息', url: 'https://baidu.com/4', rank: 4, hot_value: '3456789' },
  { platform_id: 'baidu', title: '股市行情分析', url: 'https://baidu.com/5', rank: 5, hot_value: '3012345' },
];

async function insertSampleData() {
  const client = new Client({ connectionString });

  try {
    await client.connect();
    console.log('✓ 数据库连接成功！');

    // 清空现有数据
    await client.query('DELETE FROM news_items');
    console.log('✓ 清空旧数据');

    // 插入示例数据
    for (const news of sampleNews) {
      await client.query(
        'INSERT INTO news_items (platform_id, title, url, rank, hot_value, last_crawl_time) VALUES ($1, $2, $3, $4, $5, NOW())',
        [news.platform_id, news.title, news.url, news.rank, news.hot_value]
      );
    }

    console.log(`✓ 成功插入 ${sampleNews.length} 条示例数据！`);

    // 查询验证
    const result = await client.query('SELECT COUNT(*) FROM news_items');
    console.log(`✓ 数据库中共有 ${result.rows[0].count} 条新闻`);

  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await client.end();
  }
}

insertSampleData();
