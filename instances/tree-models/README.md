# Примірник tree-models

Цей примірник шукає в книжках і статтях про моделі на деревах рішень. Дерево рішень — це модель, яка ставить запитання про ознаки
по черзі («ціна вища за 100?», «обсяг менший за середній?») і за відповідями доходить до листа з прогнозом. Одне глибоке дерево
запам'ятовує навчальні дані замість закономірності, тому дерева об'єднують в ансамблі. Випадковий ліс будує сотні дерев на
випадкових підвибірках і ознаках та усереднює їхні відповіді. Градієнтний бустинг будує дерева по черзі, і кожне наступне
виправляє помилки попередніх: так працюють XGBoost, LightGBM і CatBoost.

Примірник зібрано під проєкт, що навчає моделі XGBoost і LightGBM на ринкових даних. Тут лежить теорія: як дерево вибирає поділ, що
насправді налаштовують параметри, як чесно перевіряти модель на часових рядах і як пояснювати її прогнози. Довідники API самих
бібліотек лежать в інших примірниках: [`xgboost`](../xgboost/README.md), [`lightgbm`](../lightgbm/README.md),
[`numpy`](../numpy/README.md).

## Що всередині

**Книжки з файлів користувача** (корпус лише на цій машині, див. нижче):

| Книжка | Документів |
|---|---|
| Greenwell, Tree-Based Methods for Statistical Learning in R (CRC, 2022) | 84 |
| Zhou, Ensemble Methods: Foundations and Algorithms, 2-ге вид. (CRC, 2025) | 86 |
| Breiman, Friedman, Olshen, Stone, Classification and Regression Trees (Chapman & Hall/CRC, 1984) | 15 |
| Rokach, Maimon, Data Mining with Decision Trees: Theory and Applications, 1-ше вид. (World Scientific, 2008) | 71 |
| Genuer, Poggi, Random Forests with R (Springer, 2020) | 36 |
| Kuhn, Johnson, Applied Predictive Modeling (Springer, 2013) | 164 |
| López de Prado, Advances in Financial Machine Learning (Wiley, 2018) | 24 |
| Jansen, Hands-On Machine Learning for Algorithmic Trading (Packt, 2018) | 255 |
| Jansen, Machine Learning for Algorithmic Trading, 2-ге вид. (Packt, 2020), з EPUB | 26 |
| Géron, Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 2-ге вид. (O'Reilly, 2019) | 218 |

**Безкоштовні книжки й документація:**

| Що | Звідки | Документів |
|---|---|---|
| Louppe, Understanding Random Forests: From Theory to Practice (дисертація, Льєж, 2014) | arXiv:1407.7502 | 56 |
| Boehmke, Greenwell, Hands-On Machine Learning with R (CRC, 2020) | глави `.Rmd` репозиторію `bradleyboehmke/HOML` | 23 |
| Molnar, Interpretable Machine Learning, 3-тє вид. (2025) | глави `.qmd` репозиторію `christophM/interpretable-ml-book` | 45 |
| Kuhn, Johnson, Feature Engineering and Selection (CRC, 2019) | сайт книжки feat.engineering | 13 |
| scikit-learn User Guide: 1.10 Decision Trees і 1.11 Ensembles | scikit-learn.org, стабільна версія | 2 |

**Статті** (PDF з arXiv, сайтів журналів і авторів): Breiman, Random Forests (2001); Geurts, Ernst, Wehenkel, Extremely Randomized
Trees (2006); Meinshausen, Quantile Regression Forests (2006); Biau, Scornet, A Random Forest Guided Tour (2016); Probst, Wright,
Boulesteix про налаштування параметрів лісу (2019); Wright, Ziegler, ranger (2017); Nakandala та ін., Hummingbird (2020); Chen,
Guestrin, XGBoost (2016); Prokhorenkova та ін., CatBoost (2018); Grinsztajn, Oyallon, Varoquaux про дерева й нейромережі на
табличних даних (2022); Lundberg та ін., TreeSHAP (2020); Athey, Tibshirani, Wager, Generalized Random Forests (2019).

Усього 1318 документів, з них пошук будує 10 731 фрагмент. Фрагмент — це невеликий шматок тексту, який знаходить пошук. Документ
книжки — глава чи розділ за закладками PDF, документ статті — її розділ. PDF без закладок (Breiman 2001, Extremely Randomized Trees,
Quantile Regression Forests, дисертація Louppe) поділено на шматки по чотири сторінки з назвою «pp. N–M».

Замір `quality` на 08.11.2026 дав такі числа. Запити назвами методів знаходять потрібне 10 із 10, а модель зазвичай питає саме так.
Запити своїми словами знаходять потрібне 9 із 10.

## Чого тут немає

Цих текстів програма завантажити не може. Їх можна завантажити браузером у «Завантаження», і тоді вони додадуться:

- The Elements of Statistical Learning та An Introduction to Statistical Learning: автори роздають PDF через Google Drive з
  підтвердженням;
- Understanding Machine Learning (Shalev-Shwartz, Ben-David): сайт університету відповідає програмам сторінкою захисту;
- Probabilistic Machine Learning (Murphy): файл важить 92 МБ, а стеля одного завантаження у фабриці — 50 МБ;
- стаття LightGBM (NeurIPS 2017) і звіт Decision Forests (Microsoft Research): сайти не відповідають програмі;
- стаття Strobl та ін. про упередженість важливості ознак (2007): Springer віддає PDF лише після входу.

Формули в PDF витягуються як текст і часто розсипаються, а підписи до рисунків стоять посеред абзаців. Пояснення словами від цього
не страждає.

## Як читаються файли

Для цього примірника написано два читачі:

- `pdf-outline` ділить PDF на документи за закладками до заданої глибини, а глибші закладки робить підзаголовками. Колонтитули він
  прибирає за повторенням на краях сторінок. Сторінку, на якій бібліотека pypdf падає, він читає через PDFium (pypdfium2);
- `epub-local` бере глави EPUB у порядку читання.

## Корпус лише локально

Корпус — це тексти глав і статей, а індекс — кеш фрагментів, з якого підіймається сервер. Платні книжки не можна поширювати, тому
**корпус, індекс і файли книжок у git не потрапляють** (`corpus/`, `index/` і `raw/` у `.gitignore`). У git лежать лише
налаштування примірника, а сервер працює лише на цій машині.

**Де тексти.** Вони лежать в архіві `~/archives/docfactory/tree-models-corpus-2026-11-08.tar.gz` разом із паспортом, сховищем сирого
і файлами книжок у `raw/local/`. Копія лежить на Windows: `C:\Distr\tree-models-corpus-2026-11-08.tar.gz`. Архів звірено з диском
файл за файлом, а копію — за SHA-256. Сервер підіймається з кешу `index/passages.json` і колекції Qdrant, тому тексти йому не
потрібні.

**Як повернути тексти** перед оновленням:

```
tar -xzf ~/archives/docfactory/tree-models-corpus-2026-11-08.tar.gz -C instances/tree-models
./df tree-models smoke
```

**Якщо зникне кеш фрагментів.** Спершу поверніть тексти, а потім запустіть `./df tree-models vectors`: кеш збереться заново.

Як оновлювати примірник, описано в [UPDATE.md](UPDATE.md).

## Як запустити

```
./df tree-models serve
```

Сервер слухає порт `8961`. Під'єднати його до Claude Code можна файлом `.mcp.json` цієї теки або командою:

```
claude mcp add --transport http --scope user tree-models-docs http://127.0.0.1:8961/mcp
```

Команда для Claude Code у Windows, коли сервер працює у WSL, та сама. Перевірка: `./df tree-models smoke` і `./df tree-models quality`.
