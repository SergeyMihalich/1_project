import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"instantclient_21_3")


def ora_conect(dsn):
    user = "test"
    password = "test"
    connection = cx_Oracle.connect(user=user, password=password, dsn=dsn)
    print("Connected to Oracle Database")
    return connection


def ora_sms(id, stand):
    try:
        connection = ora_conect(stand['dsn'])
        try:
            cursor = connection.cursor()
            select_str = f"""SELECT flo.TxcNotifTemplate.CalcMessageAsString (idpSelf => t.idTPL, idpObject => t.idObject, idpReceiver => t.idReceiver, spLang => 'RU', spParam1 => t.sParam1 ) sMsg, t.*
                            FROM flo.fl_notification t
                            WHERE dtinsert >= sysdate - 2 / 24
                            AND idReceiver = (SELECT id FROM flo.fl_consultant WHERE NNUMBER = {id})
                            AND idsmsgate IS NOT NULL"""
            cursor.execute(select_str)
            sms = list(cursor)
        finally:
            cursor.close()
    finally:
        if connection is not None:
            connection.close()
    return sms


def ora_cash(login, many, provider, stand):
    try:
        connection = ora_conect(stand['dsn'])
        try:
            cursor = connection.cursor()

            select_str = f"""declare
                    t integer;
                    spvOuterID varchar2(32) := sys_guid;
                    npvAccount integer := {login}; --логин консультанта
                    fpvAmount integer  := {many} ; -- сумма начисляемых денег
            begin
              TxcError.RaiseError(
                    PcaTransaction.ChargeCommit(
                                                 spOuterID => spvOuterID,
                                                 idpProvider => {provider}, --провайдер
                                                 npAccount => npvAccount,
                                                 dtpOuter => SYSDATE,
                                                 fpAmount => fpvAmount,
                                                 idpTransaction => t )
                                  );
            end;"""
            cursor.execute(select_str)
            
        finally:
            cursor.close()
    finally:
        if connection is not None:
            connection.close()
    return many


def main():
    ora_cash('727750332', '199', '1000231828895', 'qa-test-2')


if __name__ == "__main__":
    main()
