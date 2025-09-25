# Dashboard RH - Construtora

Dashboard interativo para análise de dados de recursos humanos de uma empresa de construção civil.

## Funcionalidades

### KPIs Principais
- Total de funcionários
- Funcionários ativos
- Salário médio
- Taxa de rotatividade

### Análises Disponíveis
1. **Distribuição por Departamento** - Visualização em pizza dos funcionários por área
2. **Distribuição por Idade** - Histograma da faixa etária dos colaboradores
3. **Análise Salarial** - Box plot dos salários por departamento
4. **Métricas de Segurança** - Acidentes, uso de EPI e certificações
5. **Performance vs Treinamento** - Correlação entre avaliação e horas de treinamento
6. **Níveis de Escolaridade** - Distribuição educacional da equipe
7. **Horas de Treinamento** - Média por departamento
8. **Motivos de Desligamento** - Análise do turnover

## Como Executar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o dashboard:**
   ```bash
   python hr_dashboard.py
   ```

3. **Acessar no navegador:**
   ```
   http://localhost:8050
   ```

## Estrutura dos Dados

O dashboard analisa 160 registros de funcionários com as seguintes informações:

- **Dados Pessoais:** ID, nome, idade, sexo, escolaridade
- **Trabalho:** Cargo, departamento, obra atual, salário
- **Performance:** Avaliação, horas de treinamento, ausências
- **Segurança:** Acidentes, uso de EPI, certificações
- **Status:** Ativo/desligado, motivos de saída

## Tecnologias Utilizadas

- **Python 3.10+**
- **Dash 2.14.1** - Framework web para Python
- **Plotly 5.17.0** - Biblioteca de visualização
- **Pandas 2.1.1** - Manipulação de dados
- **NumPy 1.25.2** - Computação numérica

## Departamentos Analisados

- **Operacional** - Pedreiros, soldadores, eletricistas, etc.
- **Técnico** - Engenheiros, arquitetos, técnicos especializados
- **Administrativo** - RH, financeiro, assistentes
- **Todas as Obras** - Funcionários que atuam em múltiplos projetos

Este dashboard fornece insights valiosos para a gestão de RH, permitindo análises de performance, segurança e rotatividade da equipe de construção.