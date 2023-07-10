import { writable, derived } from "svelte/store";
import { getConnection, PARQUETS } from "./duckdb";

export const selectedItemId = writable<string>();

const getAvgPriceTableData = async (itemId: string): Promise<AvgPriceTableData> => {
  const conn = await getConnection();
  const stmt = await conn.prepare(`
            SELECT 
                category, 
                ("2018" / 100)::FLOAT AS wtAvg2018, 
                ("2019" / 100)::FLOAT AS wtAvg2019, 
                ("2020" / 100)::FLOAT AS wtAvg2020, 
                ("2021" / 100)::FLOAT AS wtAvg2021, 
                ("2022" / 100)::FLOAT AS wtAvg2022, 
                ("2023" / 100)::FLOAT AS wtAvg2023
            FROM parquet_scan(${PARQUETS.itemWeightedAvgByYear})
            WHERE item_id = ?
            ORDER BY category DESC`);
  const results = await stmt.query(itemId);
  return {
    headers: ['Type', '2023', '2022', '2021', '2020', '2019', '2018'],
    data: results.toArray()
  };
};

export const weightedAvgPrices = derived(selectedItemId, async ($selectedItemId) => {
  return await getAvgPriceTableData($selectedItemId);
})

const getBids = async (itemId: string): Promise<Bid[]> => {
  const conn = await getConnection();
  const stmt = await conn.prepare(`
    SELECT 
        contract_id AS contractId,
        letting_date AS lettingDate,
        bidder_name AS bidderName,
        quantity,
        (unit_price_cents / 100) AS unitPrice,
        category
    FROM parquet_scan(${PARQUETS.bids})
    WHERE item_id = ?
    ORDER BY category DESC`);
  const results = await stmt.query(itemId);
  return results.toArray();
}

export const bids = derived(selectedItemId, async ($selectedItemId) => {
  return await getBids($selectedItemId)
})
