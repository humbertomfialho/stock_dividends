import sqlite3

def create_new_data_base():
    connection = sqlite3.connect(database='data/automatic_stocks.db')
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Operation(
            id_negotiation int,
            type_negotiation varchar(255),
            buy_sell varchar(255),
            market_type varchar(255),
            stock_name varchar(255),
            quantity int,
            price float,
            total_value float,
            credit_debit varchar(255)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Negotiation(
            id int,
            date date,
            sell float,
            buy float,
            total_value float,
            operation_net_value float,
            settlement_tax float,
            total_cblc float,
            emolumentos float,
            total_bovespa float,
            operational_rate float,
            taxes float,
            irrf float,
            others float,
            total_costs float,
            net_value float
        );
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS Stock(
                type varchar(255),
                market_type varchar(255),
                market varchar(255),
                isin varchar(255),
                issuer_code varchar(255),
                ticker varchar(255),
                b3_name varchar(255),
                name varchar(255),
                long_name varchar(255),
                cvm_code int,
                b3_listing_segment varchar(255),
                b3_segment varchar(255),
                b3_sector varchar(255),
                b3_subsector varchar(255),
                main_activity varchar(255),
                is_b3_listed varchar(255),
                is_foreign varchar(255),
                is_state_owned varchar(255)
            );
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS Market(
                date date,
                ibov float,
                selic float,
                ipca float
            );
        '''
    )

    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS Dividends(
                payable_date date,
                record_date date,
                cvm_code int,
                type varchar(255),
                ticker varchar(255),
                amount float
            );
        '''
    )
    
    connection.commit()
    connection.close()
    return

if __name__ == '__main__':
    create_new_data_base()