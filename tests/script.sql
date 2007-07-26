Parsing: D:\lab\yadsel\yadsel\examples\test3
Upgrading...
/* Version 1 */
 CREATE TABLE AGENDA ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , CODIGO_ORIGEM VARCHAR(20) , TIPO_CONTATO CHAR(1)  DEFAULT 'T'  NOT NULL , NUMERO VARCHAR(20)  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , DESCRICAO VARCHAR(60)  );
 CREATE TABLE CELULARES ( NOVO CHAR(1)  DEFAULT 'S'  NOT NULL , OPERACAO CHAR(1)  DEFAULT '-'  NOT NULL , COBRA CHAR(1)  DEFAULT 'S'  NOT NULL , GUID_CONTRATO VARCHAR(38) , STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_EMPRESA VARCHAR(38) , VLR_CREDITO DECIMAL(8,2)  DEFAULT 0  NOT NULL , GUID_PLANO VARCHAR(38) , CALC_ACRESC CHAR(1)  DEFAULT 'S'  NOT NULL , MARCA VARCHAR(30) , NUMERO VARCHAR(10) , NUMERO_ESN VARCHAR(15) , TIPO_ACESSO CHAR(1) , GUID_PLANO_DADOS VARCHAR(38) , HERDA_PLANO_CONTRATO CHAR(1)  DEFAULT 'S'  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE , GUID_USUARIO VARCHAR(38) , TARIFA_ZERO CHAR(1)  DEFAULT 'N'  NOT NULL  );
 CREATE TABLE CELULARES_CNT ( VLR_CREDITO DECIMAL(8,2) , STATUS CHAR(1) , GUID_FATURA VARCHAR(38)  NOT NULL , GUID_EMPRESA VARCHAR(38)  NOT NULL , GUID_CELULAR VARCHAR(38)  NOT NULL , VLR_DEBITO DECIMAL(8,2) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE , DESCRICAO VARCHAR(100)  );
 CREATE TABLE CELULARES_HST ( STATUS CHAR(1) , QTD_MINUTOS INTEGER , GUID_EMPRESA VARCHAR(38) , GUID_CELULAR VARCHAR(38) , TARIFA_ZERO CHAR(1) , GUID_FATURAPLANO VARCHAR(38) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE , GUID_USUARIO VARCHAR(38)  );
 CREATE TABLE CONTRATOS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_PLANO VARCHAR(38) , GUID_OPERADORA VARCHAR(38) , NUMERO VARCHAR(20) , GUID_EMPRESA VARCHAR(38) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE , DESCRICAO VARCHAR(60)  );
 CREATE TABLE DEPARTAMENTOS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_EMPRESA VARCHAR(38) , CODIGO_EMP VARCHAR(6) , CODIGO_DEP VARCHAR(8) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE DESCRICOES_CONSUMO ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_TIPOTARIFACAO VARCHAR(38) , GUID_DESCRICAOCOTA_MOVEL VARCHAR(38) , VISIVEL CHAR(1)  DEFAULT 'S'  NOT NULL , UNIDADE VARCHAR(10) , CONDICAO BLOB SUB_TYPE 2 SEGMENT SIZE 4096 , GUIDS_MODALIDADE VARCHAR(255) , GUID_DESCRICAOCOTA_FIXO VARCHAR(38) , GUIDS_TIPOTELEFONIA VARCHAR(255) , GUID_TIPOCONSUMO VARCHAR(38) , GUIDS_TIPOPLANO VARCHAR(255) , GUIDS_TIPOLINHA VARCHAR(255) , TIPO_VALOR CHAR(1)  DEFAULT 'D'  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(100)  NOT NULL  );
 CREATE TABLE DESCRICOES_COTAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_TIPOCOTA VARCHAR(38)  NOT NULL , CONDICAO BLOB SUB_TYPE 2 SEGMENT SIZE 4096 , GUIDS_TIPOTELEFONIA VARCHAR(255) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  );
 CREATE TABLE EMPRESAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , CNPJ VARCHAR(100) , EXPIRADO CHAR(1)  DEFAULT 'N' , COMPLEMENTO VARCHAR(30) , NOME VARCHAR(60)  NOT NULL , OPERADORA CHAR(1) , BAIRRO VARCHAR(30) , CIDADE VARCHAR(30) , LOGRADOURO VARCHAR(60) , NUMERO VARCHAR(10) , CHAVE VARCHAR(100)  NOT NULL , DTA_FUNDACAO DATE , DTA_EXPIRACAO DATE , CEP VARCHAR(9) , RESPONSAVEL VARCHAR(60) , INSCEST VARCHAR(25) , GUID VARCHAR(38)  NOT NULL , ESTADO CHAR(2)  DEFAULT 'GO' , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , NOMEFANTASIA VARCHAR(60)  );
 CREATE TABLE EMPRESAS_CTT ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , TIPO_CONTATO VARCHAR(20)  DEFAULT 'R1'  NOT NULL , CONTATO VARCHAR(60)  NOT NULL , GUID_EMPRESA VARCHAR(38)  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , DESCRICAO VARCHAR(60)  );
 CREATE TABLE FATURAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , TIPO_ACESSO CHAR(1) , GUID_CONTRATO VARCHAR(38) , DTA_ALTERACAO TIMESTAMP , DATA_FINAL DATE , GUID_PLANO VARCHAR(38) , PLANO_VLR_EXCEDENTE DECIMAL(8,2)  DEFAULT 0 , ARQUIVO_TAMANHO INTEGER , PLANO_DESCRICAO VARCHAR(60) , NUMERO VARCHAR(10) , OBSERVACAO VARCHAR(255) , DATA_INICIAL DATE , MODELO_ARQUIVO VARCHAR(4)  DEFAULT 'XLS1'  NOT NULL , PLANO_VLR_FRANQUIA DECIMAL(8,2) , GUID_EMPRESA VARCHAR(38) , GUID VARCHAR(38)  NOT NULL , PLANO_QTD_FRANQUIA INTEGER , QTD_SERVICOS INTEGER , MESANO VARCHAR(20)  );
 CREATE TABLE FILTROS ( STATUS CHAR(1) , ESQUEMA VARCHAR(30) , CAMPO VARCHAR(30) , VALOR VARCHAR(255) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  );
 CREATE TABLE MODALIDADES ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_TIPOTELEFONIA VARCHAR(38) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE OPERADORAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , GUID VARCHAR(38)  NOT NULL , GUID_TIPOTELEFONIA VARCHAR(38) , DESCRICAO VARCHAR(50)  NOT NULL , OPERADORA_CSP SMALLINT  );
 CREATE TABLE PARAMETROS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , EXPORTA_AC1 CHAR(1) , DTA_VERSAOAPP DATE , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , SMTP_SERVIDOR VARCHAR(30) , SMTP_PORTA INTEGER  DEFAULT 25  NOT NULL , GUID_EMPRESA VARCHAR(38) , SMTP_SENHA VARCHAR(15) , VERSAOAPP VARCHAR(12)  DEFAULT '3.0.0.0' , PRIORIDADE INTEGER  DEFAULT 3 , SENHA VARCHAR(100)  DEFAULT 'PHONUS'  NOT NULL , LOGIN VARCHAR(15)  DEFAULT 'PHONUS'  NOT NULL , GUID VARCHAR(38)  NOT NULL , SMTP_LOGIN VARCHAR(50) , PERC_ACRESC INTEGER  DEFAULT 0  NOT NULL  );
 CREATE TABLE PLANOS ( GUID_MODALIDADE VARCHAR(38) , DSL1 DECIMAL(8,2) , DESC_CONSUMOMINIMO VARCHAR(255)  DEFAULT '' , TIPO_FRANQUIA CHAR(1)  DEFAULT 'C'  NOT NULL , TAXBLOQ DECIMAL(8,2) , VLR_UNITARIO DECIMAL(8,2)  DEFAULT 0 , GUID VARCHAR(38)  NOT NULL , DESCRICAO VARCHAR(60) , DSL2 DECIMAL(8,2) , VC2_MM_BANDA_B DECIMAL(8,2) , VC2_MM_BANDA_A DECIMAL(8,2) , VC2_MM_BANDA_D DECIMAL(8,2) , VC2_MM_BANDA_E DECIMAL(8,2) , GUID_OPERADORA VARCHAR(38) , GUID_TIPOPLANO VARCHAR(38) , ASSINATURA DECIMAL(8,2) , VLR_FRANQUIA DECIMAL(8,2) , VC3 DECIMAL(8,2) , VLR_EXCEDKBYTE DECIMAL(8,6) , VC1_MM_BANDA_E DECIMAL(8,2) , VC2_MF DECIMAL(8,2) , VC1_MM_BANDA_B DECIMAL(8,2) , VC1_MM_BANDA_A DECIMAL(8,2) , STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , VC1_MF DECIMAL(8,2) , QTD_FRANQUIA INTEGER , QTD_LINHAS INTEGER , INTRAGRUPOZERO DECIMAL(8,2) , TIPO_ACESSO CHAR(1) , VLR_EXCEDENTE DECIMAL(8,5) , VC1_MM_BANDA_D DECIMAL(8,2) , AD_INTRA_AREA_7 DECIMAL(8,2) , TIPO_TARIFACAO_INTERURBANO VARCHAR(5) , NOME_ASSINATURA_MENSAL VARCHAR(50) , DTA_ALTERACAO DATE , GUID_TIPOLINHA VARCHAR(38) , TIPO_TARIFACAO_FIXA VARCHAR(5)  );
 CREATE TABLE PLANOS_REGRAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , VLR_REGRA DECIMAL(8,5)  DEFAULT 0 , GUID_DESCRICAOCONSUMO VARCHAR(38) , LIBERADO CHAR(1)  DEFAULT 'S'  NOT NULL , GUID_PLANO VARCHAR(38) , TEXTO_REGRA VARCHAR(50) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL  );
 CREATE TABLE SERVICOS ( NUM_ORIGEM VARCHAR(10) , NUM_DESTINO VARCHAR(20) , UNIDADE VARCHAR(10) , ESTADO_DESTINO VARCHAR(2) , HORA_SERVICO VARCHAR(8) , TARIFA VARCHAR(25) , DESCRICAO VARCHAR(255) , VLR_CALCULADO DECIMAL(8,5) , GUID VARCHAR(38)  NOT NULL , TC_DESCRICAO VARCHAR(255) , TIPO VARCHAR(100) , VLR_SERVICO DECIMAL(8,5) , AREA_DESTINO INTEGER , TIPO_CONSUMO CHAR(1) , SUBGRUPO VARCHAR(255) , AREA_ORIGEM INTEGER , LINHA INTEGER , GUID_USUARIO VARCHAR(38) , STATUS CHAR(1) , PLANILHA VARCHAR(100) , DTA_SERVICO DATE , CIDADE_DESTINO VARCHAR(30) , QTD_SERVICO INTEGER , VLR_TARIFA_SERV DECIMAL(8,5) , GUID_EMPRESA VARCHAR(38) , VLR_TARIFA_CALC DECIMAL(8,5) , CONTADOR INTEGER , GUID_FATURA VARCHAR(38) , DDD_ORIGEM VARCHAR(2) , DDD_DESTINO VARCHAR(2) , DESTINATARIO VARCHAR(60) , CIDADE_ORIGEM VARCHAR(30) , INTRA_GRUPO CHAR(1) , FATURA VARCHAR(10) , GUID_PLANOREGRA VARCHAR(38) , GUID_DESCRICAOCONSUMO VARCHAR(38) , OPERADORA VARCHAR(2) , ESTADO_ORIGEM VARCHAR(2) , GUID_CELULAR VARCHAR(38) , GRUPO VARCHAR(255) , MARCADO CHAR(1) , DTA_ALTERACAO DATE  );
 CREATE TABLE TBLKRE ( ENDKRE VARCHAR(15) , VLRKRE VARCHAR(80) , TIPKRE INTEGER  NOT NULL , DTAKRE CHAR(8) , STSKRE CHAR(1)  DEFAULT 'A'  NOT NULL  );
 CREATE TABLE TIPOS_CONSUMO ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID VARCHAR(38)  NOT NULL , CONDICAO BLOB SUB_TYPE 2 SEGMENT SIZE 4096 , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE TIPOS_COTAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID VARCHAR(38)  NOT NULL , CONDICAO BLOB SUB_TYPE 2 SEGMENT SIZE 4096 , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  );
 CREATE TABLE TIPOS_LINHA ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID_TIPOTELEFONIA VARCHAR(38) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE TIPOS_PLANO ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , GUID VARCHAR(38)  NOT NULL , GUID_TIPOTELEFONIA VARCHAR(38) , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE TIPOS_TELEFONIA ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , DESCRICAO VARCHAR(50)  NOT NULL  );
 CREATE TABLE USUARIOS ( COMPLEMENTO VARCHAR(30) , BAIRRO VARCHAR(30) , CPF VARCHAR(100) , ORGAO_EXP VARCHAR(10) , EXPORTAR_AC1 CHAR(1)  DEFAULT 'N'  NOT NULL , GUID VARCHAR(38)  NOT NULL , ACESSO CHAR(1)  DEFAULT 'N'  NOT NULL , DTA_EXPEDICAO DATE , ESTADO CHAR(2) , CIDADE VARCHAR(30) , EXPORTAR_EXTRATO CHAR(1)  DEFAULT 'S'  NOT NULL , EXPORTAR_PDF CHAR(1)  DEFAULT 'S'  NOT NULL , RG VARCHAR(15) , CEP VARCHAR(9) , GUID_DEPARTAMENTO VARCHAR(38) , STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , LOGRADOURO VARCHAR(60) , NUMERO VARCHAR(10) , GUID_EMPRESA VARCHAR(38) , CONTA_CONTABIL VARCHAR(7) , DTA_NASC DATE , CONTA_CORRENTE VARCHAR(10) , NOME VARCHAR(60) , EXPORTAR_COMUNICADO CHAR(1)  DEFAULT 'N'  NOT NULL , MATRICULA VARCHAR(20) , DTA_ALTERACAO DATE  );
 CREATE TABLE USUARIOS_ACE ( CONTRATOS CHAR(1)  DEFAULT 'N'  NOT NULL , ICONE VARCHAR(250) , DEPARTAMENTOS CHAR(1)  DEFAULT 'N'  NOT NULL , GUID VARCHAR(38)  NOT NULL , PLANOS CHAR(1)  DEFAULT 'N'  NOT NULL , EMPRESA VARCHAR(100)  DEFAULT 'N'  NOT NULL , ANALISE CHAR(1)  DEFAULT 'N'  NOT NULL , AGENDA CHAR(1)  DEFAULT 'N'  NOT NULL , PARAMETROS CHAR(1)  DEFAULT 'N'  NOT NULL , STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , EXPORTACAOC CHAR(1)  DEFAULT 'N'  NOT NULL , FATURAS CHAR(1)  DEFAULT 'N'  NOT NULL , CONSULTA CHAR(1)  DEFAULT 'N'  NOT NULL , USUARIOS CHAR(1)  DEFAULT 'N'  NOT NULL , EXPORTACAOU CHAR(1)  DEFAULT 'N'  NOT NULL , CELULARES CHAR(1)  DEFAULT 'S'  NOT NULL , RELATORIOS CHAR(1)  DEFAULT 'N'  NOT NULL , IMPORTACAO CHAR(1)  DEFAULT 'N'  NOT NULL , SENHA VARCHAR(100) , BACKUP CHAR(1)  DEFAULT 'N'  NOT NULL , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL  );
 CREATE TABLE USUARIOS_CTT ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , TIPO_CONTATO VARCHAR(20)  DEFAULT 'R1'  NOT NULL , CONTATO VARCHAR(60)  NOT NULL , DESCRICAO VARCHAR(60) , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  DEFAULT 'CURRENT_DATE'  NOT NULL , GUID_USUARIO VARCHAR(38)  NOT NULL  );
 CREATE TABLE USUARIOS_REGRAS ( STATUS CHAR(1)  DEFAULT 'A'  NOT NULL , LIBERADO CHAR(1)  DEFAULT 'S'  NOT NULL , QTD_MINUTOS INTEGER , VLR_LIBERADO DECIMAL(8,2) , GUID_DESCRICAOCOTA VARCHAR(38)  NOT NULL , GUID VARCHAR(38)  NOT NULL , DTA_ALTERACAO DATE  NOT NULL , GUID_USUARIO VARCHAR(38)  NOT NULL  );
 
            DECLARE EXTERNAL FUNCTION CHARINDEX
                CSTRING(254),
                CSTRING(254)
                RETURNS INTEGER BY VALUE
                ENTRY_POINT 'CharIndex' MODULE_NAME 'PhonusFuncs'
            ;
 SET TERM ^ ;

            CREATE PROCEDURE TESTE (
                GUID_USUARIO VARCHAR(38),
                GUID_CELULAR VARCHAR(38))
            RETURNS (
                NUMERO VARCHAR(10))
            AS
            begin
                /* Procedure Text */
                for
                select numero
                from celulares
                where guid_usuario = :guid_usuario
                  and guid = :guid_celular
                into :numero do
                    suspend;
            end
            ^
SET TERM ; ^

 ALTER TABLE AGENDA                     ADD CONSTRAINT PK_AGENDA                     PRIMARY KEY (GUID);
 ALTER TABLE CELULARES                     ADD CONSTRAINT PK_CELULARES                     PRIMARY KEY (GUID);
 ALTER TABLE CELULARES_CNT                     ADD CONSTRAINT PK_CELULARES_CNT                     PRIMARY KEY (GUID);
 ALTER TABLE CELULARES_HST                     ADD CONSTRAINT PK_CELULARES_HST                     PRIMARY KEY (GUID);
 ALTER TABLE CONTRATOS                     ADD CONSTRAINT PK_CONTRATOS                     PRIMARY KEY (GUID);
 ALTER TABLE DEPARTAMENTOS                     ADD CONSTRAINT PK_DEPARTAMENTOS                     PRIMARY KEY (GUID);
 ALTER TABLE DESCRICOES_CONSUMO                     ADD CONSTRAINT PK_DESCRICOES_CONSUMO                     PRIMARY KEY (GUID);
 ALTER TABLE DESCRICOES_COTAS                     ADD CONSTRAINT PK_DESCRICOES_COTAS                     PRIMARY KEY (GUID);
 ALTER TABLE EMPRESAS                     ADD CONSTRAINT PK_EMPRESAS                     PRIMARY KEY (GUID);
 ALTER TABLE EMPRESAS_CTT                     ADD CONSTRAINT PK_EMPRESAS_CTT                     PRIMARY KEY (GUID);
 ALTER TABLE FATURAS                     ADD CONSTRAINT PK_FATURAS                     PRIMARY KEY (GUID);
 ALTER TABLE FILTROS                     ADD CONSTRAINT PK_FILTROS                     PRIMARY KEY (GUID);
 ALTER TABLE MODALIDADES                     ADD CONSTRAINT PK_MODALIDADES                     PRIMARY KEY (GUID);
 ALTER TABLE OPERADORAS                     ADD CONSTRAINT PK_OPERADORAS                     PRIMARY KEY (GUID);
 ALTER TABLE PARAMETROS                     ADD CONSTRAINT PK_PARAMETROS                     PRIMARY KEY (GUID);
 ALTER TABLE PLANOS                     ADD CONSTRAINT PK_PLANOS                     PRIMARY KEY (GUID);
 ALTER TABLE PLANOS_REGRAS                     ADD CONSTRAINT PK_PLANOS_REGRAS                     PRIMARY KEY (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT PK_SERVICOS                     PRIMARY KEY (GUID);
 ALTER TABLE TBLKRE                     ADD CONSTRAINT PK_TBLKRE                     PRIMARY KEY (TIPKRE);
 ALTER TABLE TIPOS_CONSUMO                     ADD CONSTRAINT PK_TIPOS_CONSUMO                     PRIMARY KEY (GUID);
 ALTER TABLE TIPOS_COTAS                     ADD CONSTRAINT PK_TIPOS_COTAS                     PRIMARY KEY (GUID);
 ALTER TABLE TIPOS_LINHA                     ADD CONSTRAINT PK_TIPOS_LINHA                     PRIMARY KEY (GUID);
 ALTER TABLE TIPOS_PLANO                     ADD CONSTRAINT PK_TIPOS_PLANO                     PRIMARY KEY (GUID);
 ALTER TABLE TIPOS_TELEFONIA                     ADD CONSTRAINT PK_TIPOS_TELEFONIA                     PRIMARY KEY (GUID);
 ALTER TABLE USUARIOS                     ADD CONSTRAINT PK_USUARIOS                     PRIMARY KEY (GUID);
 ALTER TABLE USUARIOS_ACE                     ADD CONSTRAINT PK_USUARIOS_ACE                     PRIMARY KEY (GUID);
 ALTER TABLE USUARIOS_CTT                     ADD CONSTRAINT PK_USUARIOS_CTT                     PRIMARY KEY (GUID);
 ALTER TABLE USUARIOS_REGRAS                     ADD CONSTRAINT PK_USUARIOS_REGRAS                     PRIMARY KEY (GUID);
 ALTER TABLE CELULARES                     ADD CONSTRAINT FK_CELULARES_CONTRATOS                     FOREIGN KEY (GUID_CONTRATO)                     REFERENCES CONTRATOS (GUID);
 ALTER TABLE CELULARES                     ADD CONSTRAINT FK_CELULARES_USUARIOS                     FOREIGN KEY (GUID_USUARIO)                     REFERENCES USUARIOS (GUID);
 ALTER TABLE CONTRATOS                     ADD CONSTRAINT FK_CONTRATOS_PLANOS                     FOREIGN KEY (GUID_PLANO)                     REFERENCES PLANOS (GUID);
 ALTER TABLE CONTRATOS                     ADD CONSTRAINT FK_CONTRATOS_OPERADORAS                     FOREIGN KEY (GUID_OPERADORA)                     REFERENCES OPERADORAS (GUID);
 ALTER TABLE DEPARTAMENTOS                     ADD CONSTRAINT FK_DEPARTAMENTOS_EMPRESAS                     FOREIGN KEY (GUID_EMPRESA)                     REFERENCES EMPRESAS (GUID);
 ALTER TABLE DESCRICOES_CONSUMO                     ADD CONSTRAINT FK_DESCRICOES_CONSUMO_TIP_CONS                     FOREIGN KEY (GUID_TIPOCONSUMO)                     REFERENCES TIPOS_CONSUMO (GUID);
 ALTER TABLE DESCRICOES_COTAS                     ADD CONSTRAINT FK_DESCRICOES_COTAS_TIPOS_COTAS                     FOREIGN KEY (GUID_TIPOCOTA)                     REFERENCES TIPOS_COTAS (GUID);
 ALTER TABLE DESCRICOES_COTAS                     ADD CONSTRAINT FK_DESCRICOES_COTAS_TIP_COT                     FOREIGN KEY (GUID_TIPOCOTA)                     REFERENCES TIPOS_COTAS (GUID);
 ALTER TABLE EMPRESAS_CTT                     ADD CONSTRAINT FK_EMPRESAS_CTT_EMPRESAS                     FOREIGN KEY (GUID_EMPRESA)                     REFERENCES EMPRESAS (GUID);
 ALTER TABLE FATURAS                     ADD CONSTRAINT FK_FATURAS_PLANOS                     FOREIGN KEY (GUID_PLANO)                     REFERENCES PLANOS (GUID);
 ALTER TABLE FATURAS                     ADD CONSTRAINT FK_FATURAS_CONTRATOS                     FOREIGN KEY (GUID_CONTRATO)                     REFERENCES CONTRATOS (GUID);
 ALTER TABLE MODALIDADES                     ADD CONSTRAINT FK_MODALIDADES_TIPOS_TELEFONIA                     FOREIGN KEY (GUID_TIPOTELEFONIA)                     REFERENCES TIPOS_TELEFONIA (GUID);
 ALTER TABLE OPERADORAS                     ADD CONSTRAINT FK_OPERADORAS_TIPOS_TELEFONIA                     FOREIGN KEY (GUID_TIPOTELEFONIA)                     REFERENCES TIPOS_TELEFONIA (GUID);
 ALTER TABLE PARAMETROS                     ADD CONSTRAINT FK_PARAMETROS_EMPRESAS                     FOREIGN KEY (GUID_EMPRESA)                     REFERENCES EMPRESAS (GUID);
 ALTER TABLE PLANOS                     ADD CONSTRAINT FK_PLANOS_MODALIDADES                     FOREIGN KEY (GUID_MODALIDADE)                     REFERENCES MODALIDADES (GUID);
 ALTER TABLE PLANOS                     ADD CONSTRAINT FK_PLANOS_OPERADORAS                     FOREIGN KEY (GUID_OPERADORA)                     REFERENCES OPERADORAS (GUID);
 ALTER TABLE PLANOS                     ADD CONSTRAINT FK_PLANOS_TIPOS_LINHA                     FOREIGN KEY (GUID_TIPOLINHA)                     REFERENCES TIPOS_LINHA (GUID);
 ALTER TABLE PLANOS                     ADD CONSTRAINT FK_PLANOS_TIPOS_PLANO                     FOREIGN KEY (GUID_TIPOPLANO)                     REFERENCES TIPOS_PLANO (GUID);
 ALTER TABLE PLANOS_REGRAS                     ADD CONSTRAINT FK_PLANOS_REGRAS_PLANOS                     FOREIGN KEY (GUID_PLANO)                     REFERENCES PLANOS (GUID);
 ALTER TABLE PLANOS_REGRAS                     ADD CONSTRAINT FK_PLANOS_REGRAS_DESC_CONS                     FOREIGN KEY (GUID_DESCRICAOCONSUMO)                     REFERENCES DESCRICOES_CONSUMO (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT FK_SERVICOS_DESCRICOES_CONSUMO                     FOREIGN KEY (GUID_DESCRICAOCONSUMO)                     REFERENCES DESCRICOES_CONSUMO (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT FK_SERVICOS_USUARIOS                     FOREIGN KEY (GUID_USUARIO)                     REFERENCES USUARIOS (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT FK_SERVICOS_FATURAS                     FOREIGN KEY (GUID_FATURA)                     REFERENCES FATURAS (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT FK_SERVICOS_CELULARES                     FOREIGN KEY (GUID_CELULAR)                     REFERENCES CELULARES (GUID);
 ALTER TABLE SERVICOS                     ADD CONSTRAINT FK_SERVICOS_PLANOS_REGRAS                     FOREIGN KEY (GUID_PLANOREGRA)                     REFERENCES PLANOS_REGRAS (GUID);
 ALTER TABLE TIPOS_LINHA                     ADD CONSTRAINT FK_TIPOS_LINHA_TIP_TEL                     FOREIGN KEY (GUID_TIPOTELEFONIA)                     REFERENCES TIPOS_TELEFONIA (GUID);
 ALTER TABLE TIPOS_PLANO                     ADD CONSTRAINT FK_TIPOS_PLANO_TIP_TEL                     FOREIGN KEY (GUID_TIPOTELEFONIA)                     REFERENCES TIPOS_TELEFONIA (GUID);
 ALTER TABLE USUARIOS                     ADD CONSTRAINT FK_USUARIOS_DEPARTAMENTOS                     FOREIGN KEY (GUID_DEPARTAMENTO)                     REFERENCES DEPARTAMENTOS (GUID);
 ALTER TABLE USUARIOS_ACE                     ADD CONSTRAINT FK_USUARIOS_ACE_USUARIOS                     FOREIGN KEY (GUID)                     REFERENCES USUARIOS (GUID);
 ALTER TABLE USUARIOS_CTT                     ADD CONSTRAINT FK_USUARIOS_CTT_USUARIOS                     FOREIGN KEY (GUID_USUARIO)                     REFERENCES USUARIOS (GUID);
 ALTER TABLE USUARIOS_REGRAS                     ADD CONSTRAINT FK_USUARIOS_REGRAS_DESC_COT                     FOREIGN KEY (GUID_DESCRICAOCOTA)                     REFERENCES DESCRICOES_COTAS (GUID);
 ALTER TABLE USUARIOS_REGRAS                     ADD CONSTRAINT FK_USUARIOS_REGRAS_USUARIOS                     FOREIGN KEY (GUID_USUARIO)                     REFERENCES USUARIOS (GUID);