
const request = require("request-promise");
const cheerio = require("cheerio");
const {Pool, Client} = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'scrapingdb',
  password: 'eBaye1er',
  port: '5432',
  max: 100

});

async function scapedData() {
 const result = await request.get("https://www.linternaute.com/ville/classement/villes/immigres");
 const $ = cheerio.load(result);

 const myScapedData = [];

 $("#jStickySize > div.hidden.marB20 > table > tbody > tr").each((index, element) => {

   if (index === 0)
   return true;

   const tds = $(element).find("td");

   const rang = $(tds[0]).text();
   const ville = $(tds[1]).text();
   const per = $(tds[2]).text();

   const tableRow = {rang, ville, per};

   myScapedData.push(tableRow);
   values = [tableRow.rang, tableRow.ville, tableRow.per];

   pool.query(
    `INSERT INTO table_people (rang, ville, percentage) VALUES($1, $2, $3)`,
    values,
    (err, res) => {
      console.log(err, res);
     // pool.end();
    }
   );

 });
}

scapedData();