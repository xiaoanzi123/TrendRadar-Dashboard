import pg from 'pg';
import fs from 'fs';

const { Client } = pg;

const connectionString = 'postgresql://postgres:CAF@sbb1991328@db.sqnfcrywcddssjopdcde.supabase.co:5432/postgres';

async function setupDatabase() {
  const client = new Client({ connectionString });

  try {
    console.log('正在连接数据库...');
    await client.connect();
    console.log('✓ 数据库连接成功！');

    console.log('正在读取 SQL 脚本...');
    const sql = fs.readFileSync('./supabase-schema.sql', 'utf8');

    console.log('正在执行 SQL 脚本...');
    await client.query(sql);
    console.log('✓ SQL 脚本执行成功！');

    console.log('\n数据库设置完成！');
  } catch (err) {
    console.error('错误:', err.message);
    process.exit(1);
  } finally {
    await client.end();
  }
}

setupDatabase();
