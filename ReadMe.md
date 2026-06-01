## Arquitetura da Solução

A plataforma foi construída utilizando uma arquitetura de Engenharia de Dados baseada em Data Lake, Data Warehouse e Observabilidade.

### Fluxo de Dados

```text
Scrapers/APIs
      │
      ▼
 Raw JSON (Data Lake)
      │
      ▼
 PostgreSQL
(Bronze / Silver / Gold)
      │
      ▼
 Grafana
(Dashboards e Analytics)
```

---

### Data Lake

Os dados coletados são armazenados em arquivos JSON para preservação dos registros originais.

Estrutura:

```text
data_lake/

├── raw/
├── clean/
└── curated/
```

Objetivos:

* Preservação dos dados originais
* Reprocessamento futuro
* Auditoria
* Backup das coletas

---

### PostgreSQL

O PostgreSQL atua como a principal camada de processamento e disponibilização dos dados.

Além de armazenar as informações, ele é responsável pela organização dos dados em diferentes níveis de maturidade para facilitar consultas analíticas e integração com o Grafana.

#### Bronze Layer (jobs_raw)

Armazena os dados exatamente como foram coletados.

Características:

* Dados originais
* JSON completo da vaga
* Histórico de ingestão
* Rastreabilidade

#### Silver Layer (jobs_processed)

Armazena os dados normalizados.

Características:

* Limpeza de campos
* Padronização
* Preparação para análises

#### Gold Layer (jobs_curated)

Armazena os dados otimizados para dashboards.

Características:

* Consultas rápidas
* Menor volume de processamento
* Estrutura pronta para visualização

#### Dimensões

Tabela:

* dim_company

Responsável por consolidar informações das empresas coletadas.

---

### Grafana

O Grafana consome os dados diretamente do PostgreSQL.

Principais funcionalidades:

* Listagem de vagas
* Empresas monitoradas
* Ranking de empresas contratando
* Filtros por localização
* Links clicáveis para candidatura
* Monitoramento da execução do pipeline

O PostgreSQL foi modelado especificamente para fornecer consultas eficientes ao Grafana, reduzindo a necessidade de processamento na camada de visualização.

---

### Observabilidade

Tabela:

* pipeline_runs

Permite acompanhar:

* Execuções do ETL
* Status das coletas
* Quantidade de vagas processadas
* Falhas encontradas
* Tempo de execução

Essa abordagem facilita a manutenção, auditoria e expansão futura da plataforma.
