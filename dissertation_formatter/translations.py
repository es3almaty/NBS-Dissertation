from __future__ import annotations

TEXT={
"en":{
"resubmit_title":"RESUBMIT BEFORE FORMATTING","ready_title":"READY","conditional_title":"CONDITIONAL",
"resubmit_notice":"Formatting was not performed because the submitted dissertation is missing more than two mandatory structural components. Please correct all issues listed in this report and resubmit the document.",
"status":"Submission status","summary":"Executive summary","critical":"Critical structural requirements","corrected":"Automatically corrected items","actions":"Student action required","unalterable":"Detected but not safely alterable","internal":"Internal inconsistencies requiring student review","tables":"Tables and figures","refs":"References and citations","length":"Length and structural recommendations","not_checked":"Items not checked by the system","responsibility":"Student responsibility statement","checklist":"Resubmission checklist",
"reference_disclaimer":"References have been formatted using the information supplied in the dissertation. The system has not verified that the sources exist, that bibliographic information is accurate, or that the citations accurately represent the cited material. Responsibility for reference accuracy remains with the student.",
"integrity":"The system does not assess academic merit, methodology quality, factual truth, plagiarism, AI writing, or whether research results are correct. It does not invent missing sources or dissertation content.",
"source_note":"Policy basis: Narxoz Master's Project Regulation controls where it conflicts with the Narxoz APA 7 guidance. APA guidance is used only where the Regulation defers to it or is silent.",
},
"ru":{
"resubmit_title":"ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ И ПОВТОРНАЯ ЗАГРУЗКА","ready_title":"ГОТОВО","conditional_title":"УСЛОВНО ГОТОВО",
"resubmit_notice":"Форматирование не выполнялось, поскольку в представленной работе отсутствуют более двух обязательных структурных компонентов. Исправьте все замечания, перечисленные в этом отчете, и повторно загрузите документ.",
"status":"Статус представленной работы","summary":"Краткое резюме проверки","critical":"Критические структурные требования","corrected":"Автоматически исправленные элементы","actions":"Требуются действия студента","unalterable":"Обнаружено, но небезопасно изменять автоматически","internal":"Внутренние несоответствия, требующие проверки студентом","tables":"Таблицы и рисунки","refs":"Ссылки и список литературы","length":"Рекомендации по объему и структуре","not_checked":"Что система не проверяет","responsibility":"Ответственность студента","checklist":"Контрольный список для повторной подачи",
"reference_disclaimer":"Список литературы был оформлен с использованием информации, представленной в магистерском проекте. Система не проверяла существование источников, точность библиографических данных или соответствие цитат содержанию цитируемых материалов. Ответственность за точность ссылок и библиографических данных несет студент.",
"integrity":"Система не оценивает академическое качество, методологию, фактическую достоверность, плагиат, использование ИИ или правильность результатов исследования. Система не создает отсутствующие источники или содержание магистерского проекта.",
"source_note":"Нормативная основа: при конфликте Положение о магистерском проекте Нархоз имеет приоритет над руководством Нархоз по APA 7. Руководство APA применяется только там, где Положение прямо отсылает к нему или не регулирует вопрос.",
},
"kk":{
"resubmit_title":"ТҮЗЕТУ ЖӘНЕ ҚАЙТА ЖҮКТЕУ ҚАЖЕТ","ready_title":"ДАЙЫН","conditional_title":"ШАРТТЫ ТҮРДЕ ДАЙЫН",
"resubmit_notice":"Ұсынылған жұмыста екіден көп міндетті құрылымдық компонент болмағандықтан форматтау орындалмады. Осы есепте көрсетілген барлық мәселелерді түзетіп, құжатты қайта жүктеңіз.",
"status":"Жұмыстың мәртебесі","summary":"Тексерудің қысқаша қорытындысы","critical":"Міндетті құрылымдық талаптар","corrected":"Автоматты түрде түзетілген элементтер","actions":"Студент әрекеті қажет","unalterable":"Анықталды, бірақ автоматты өзгерту қауіпсіз емес","internal":"Студенттің тексеруін талап ететін ішкі сәйкессіздіктер","tables":"Кестелер мен суреттер","refs":"Сілтемелер және әдебиеттер тізімі","length":"Көлем мен құрылым бойынша ұсынымдар","not_checked":"Жүйе тексермейтін мәселелер","responsibility":"Студенттің жауапкершілігі","checklist":"Қайта тапсыру тізімі",
"reference_disclaimer":"Әдебиеттер тізімі магистрлік жобада берілген ақпарат негізінде рәсімделді. Жүйе дереккөздердің бар-жоғын, библиографиялық мәліметтердің дұрыстығын немесе дәйексөздердің сілтеме жасалған материал мазмұнына сәйкестігін тексерген жоқ. Сілтемелер мен библиографиялық мәліметтердің дұрыстығына студент жауапты.",
"integrity":"Жүйе академиялық сапаны, әдіснаманы, фактілердің дұрыстығын, плагиатты, ИИ қолдануын немесе зерттеу нәтижелерінің дұрыстығын бағаламайды. Жүйе жоқ дереккөздерді немесе магистрлік жоба мәтінін жасамайды.",
"source_note":"Нормативтік негіз: қайшылық болған жағдайда Narxoz магистрлік жоба туралы ережесі Narxoz APA 7 нұсқаулығынан басым. APA нұсқаулығы Ереже тікелей сілтеме жасаған немесе мәселені реттемеген жағдайда ғана қолданылады.",
}}

def tr(lang,key):
    return TEXT.get(lang,TEXT["en"]).get(key,TEXT["en"].get(key,key))

REPORT_TEXT = {
"en": {
"subtitle":"Narxoz Master's Dissertation / Project Compliance Report","file":"File","status_label":"Status","missing":"Missing critical components",
"engine_summary":"The engine found {missing} missing applicable critical component(s), {major} critical/major finding(s), and classified {tables} Word table(s). Citation system: {citation}.",
"provisional_summary":"The evidence-based provisional audit records {missing} missing applicable critical component(s), {major} critical/major finding(s), and {tables} table record(s). The OOXML engine was not executed on this source file. Citation system: {citation}.",
"component":"Component","component_status":"Status","applicable":"Applicable","evidence":"Evidence / note","yes":"Yes","no":"No",
"no_auto":"None. Formatting was not performed in this processing state.","no_major":"No critical or major unresolved findings were detected.","none":"None identified.",
"no_internal":"No internal inconsistency was detected by the implemented deterministic checks. This is not a guarantee that none exist.",
"no_tables":"No Word tables detected.","table_check_not_executed":"OOXML table classification was not executed for this source file.","no_risk":"No structural risk signal.",
"citation_line":"Detected citation system: {citation}. References section present: {present}.","numeric_line":"Detected numeric citation numbers: {numbers}",
"length_note":"The Regulation recommends 50–70 pages excluding appendices and annotations. DOCX XML analysis does not provide a reliable final Word pagination count; page-length compliance should therefore be treated as advisory unless a layout render is available.",
"sections_note":"Detected visible major numbered sections: {count}. The Regulation states that the main part should, as a rule, consist of three sections; deviations are flagged for confirmation rather than automatically restructured.",
"not_checked_more":"The engine does not verify external source existence, factual accuracy, plagiarism, AI authorship, research validity, or whether a contradictory value is the correct one.",
"student_resp":"The student remains responsible for the accuracy and objectivity of the dissertation data, results, conclusions, citations, and supplied bibliographic metadata.",
"add_component":"Add/correct mandatory component: {component}","review":"Review: {title}","reupload":"Re-upload the corrected DOCX for a new full audit.",
"technical_note":"Technical identifiers (rule codes and deterministic classifications) are retained where useful for auditability."
},
"ru": {
"subtitle":"Отчет о соответствии магистерского проекта требованиям Нархоз","file":"Файл","status_label":"Статус","missing":"Отсутствующие критические компоненты",
"engine_summary":"Система выявила отсутствующих обязательных компонентов: {missing}; критических/существенных замечаний: {major}; классифицировано таблиц Word: {tables}. Система цитирования: {citation}.",
"provisional_summary":"Предварительная проверка по доступным данным фиксирует отсутствующих обязательных компонентов: {missing}; критических/существенных замечаний: {major}; записей о таблицах: {tables}. OOXML-движок не выполнялся на исходном DOCX. Система цитирования: {citation}.",
"component":"Компонент","component_status":"Статус","applicable":"Применимо","evidence":"Основание / примечание","yes":"Да","no":"Нет",
"no_auto":"Нет. В данном статусе форматирование не выполнялось.","no_major":"Критических или существенных нерешенных замечаний не обнаружено.","none":"Не выявлено.",
"no_internal":"Реализованные детерминированные проверки не выявили внутренних несоответствий. Это не гарантирует их полного отсутствия.",
"no_tables":"Таблицы Word не обнаружены.","table_check_not_executed":"OOXML-классификация таблиц для этого исходного файла не выполнялась.","no_risk":"Структурных признаков риска не обнаружено.",
"citation_line":"Определенная система цитирования: {citation}. Раздел списка литературы присутствует: {present}.","numeric_line":"Обнаруженные номера числовых ссылок: {numbers}",
"length_note":"Положение рекомендует объем 50–70 страниц без учета приложений и аннотаций. Анализ XML-файла DOCX не дает надежного итогового количества страниц Word, поэтому проверка объема носит рекомендательный характер, если отдельный рендер макета не выполнен.",
"sections_note":"Обнаружено основных нумерованных разделов: {count}. Положение указывает, что основная часть, как правило, состоит из трех разделов; отклонение требует подтверждения, но не исправляется автоматической перестройкой.",
"not_checked_more":"Система не проверяет существование внешних источников, фактическую достоверность, плагиат, авторство ИИ, валидность исследования и не определяет, какое из противоречащих значений является правильным.",
"student_resp":"Студент несет ответственность за точность и объективность данных, результатов, выводов, ссылок и предоставленных библиографических сведений.",
"add_component":"Добавить/исправить обязательный компонент: {component}","review":"Проверить: {title}","reupload":"Повторно загрузить исправленный DOCX для новой полной проверки.",
"technical_note":"Технические идентификаторы правил и детерминированные классификации сохраняются там, где это полезно для аудита."
},
"kk": {
"subtitle":"Narxoz магистрлік жобасының талаптарға сәйкестік есебі","file":"Файл","status_label":"Мәртебе","missing":"Жетіспейтін міндетті компоненттер",
"engine_summary":"Жүйе {missing} жетіспейтін міндетті компонентті, {major} маңызды/сыни ескертуді анықтады және {tables} Word кестесін жіктеді. Дәйексөз жүйесі: {citation}.",
"provisional_summary":"Қолжетімді деректерге негізделген алдын ала тексеру {missing} жетіспейтін міндетті компонентті, {major} маңызды/сыни ескертуді және {tables} кесте жазбасын тіркеді. Бастапқы DOCX үшін OOXML қозғалтқышы орындалмады. Дәйексөз жүйесі: {citation}.",
"component":"Компонент","component_status":"Мәртебе","applicable":"Қолданылады","evidence":"Дәлел / ескерту","yes":"Иә","no":"Жоқ",
"no_auto":"Жоқ. Осы мәртебеде форматтау орындалмады.","no_major":"Шешілмеген сыни немесе маңызды ескертулер анықталмады.","none":"Анықталмады.",
"no_internal":"Іске асырылған детерминирленген тексерулер ішкі сәйкессіздікті анықтамады. Бұл олардың мүлдем жоқ екеніне кепілдік бермейді.",
"no_tables":"Word кестелері анықталмады.","table_check_not_executed":"Осы бастапқы файл үшін OOXML кесте жіктеуі орындалмады.","no_risk":"Құрылымдық тәуекел белгісі анықталмады.",
"citation_line":"Анықталған дәйексөз жүйесі: {citation}. Әдебиеттер тізімі бар: {present}.","numeric_line":"Анықталған сандық сілтемелер: {numbers}",
"length_note":"Ереже қосымшалар мен аннотацияларды есептемегенде 50–70 бетті ұсынады. DOCX XML талдауы Word-тағы түпкілікті бет санын сенімді анықтамайды, сондықтан макет бөлек рендерленбесе, көлем жөніндегі тексеру ұсынымдық сипатта болады.",
"sections_note":"Негізгі нөмірленген бөлімдер саны: {count}. Ережеге сәйкес негізгі бөлім әдетте үш бөлімнен тұрады; ауытқу автоматты қайта құрылымдаудың орнына растауды талап етеді.",
"not_checked_more":"Жүйе сыртқы дереккөздердің бар-жоғын, фактілердің дұрыстығын, плагиатты, ИИ авторлығын, зерттеу валидтілігін немесе қайшылықты мәндердің қайсысы дұрыс екенін тексермейді.",
"student_resp":"Деректердің, нәтижелердің, қорытындылардың, сілтемелердің және берілген библиографиялық мәліметтердің дәлдігі мен объективтілігі үшін студент жауап береді.",
"add_component":"Міндетті компонентті қосу/түзету: {component}","review":"Тексеру: {title}","reupload":"Түзетілген DOCX файлын жаңа толық тексеру үшін қайта жүктеу.",
"technical_note":"Аудит үшін пайдалы болған жағдайда техникалық ереже идентификаторлары мен детерминирленген жіктеулер сақталады."
}}

COMPONENT_NAMES = {
"en":{"Title page":"Title page","Contents":"Contents","Project Summary":"Project Summary","Three-language annotation set":"Three-language annotation set","Main body":"Main body","Conclusion":"Conclusion","References":"References","Appendices":"Appendices"},
"ru":{"Title page":"Титульный лист","Contents":"Содержание","Project Summary":"Резюме проекта","Three-language annotation set":"Аннотации на трех языках","Main body":"Основная часть","Conclusion":"Заключение","References":"Список использованной литературы","Appendices":"Приложения"},
"kk":{"Title page":"Титулдық бет","Contents":"Мазмұны","Project Summary":"Жоба түйіндемесі","Three-language annotation set":"Үш тілдегі аннотациялар","Main body":"Негізгі бөлім","Conclusion":"Қорытынды","References":"Пайдаланылған әдебиеттер","Appendices":"Қосымшалар"}}

COMPONENT_STATUS = {
"en":{"PRESENT_COMPLIANT":"PRESENT_COMPLIANT","PRESENT_NONCOMPLIANT":"PRESENT_NONCOMPLIANT","MISSING":"MISSING"},
"ru":{"PRESENT_COMPLIANT":"ПРИСУТСТВУЕТ / СООТВЕТСТВУЕТ","PRESENT_NONCOMPLIANT":"ПРИСУТСТВУЕТ / НЕ СООТВЕТСТВУЕТ","MISSING":"ОТСУТСТВУЕТ"},
"kk":{"PRESENT_COMPLIANT":"БАР / СӘЙКЕС","PRESENT_NONCOMPLIANT":"БАР / СӘЙКЕС ЕМЕС","MISSING":"ЖОҚ"}}

SUBMISSION_STATUS = {
"en":{"READY":"READY","CONDITIONAL":"CONDITIONAL","RESUBMIT":"RESUBMIT"},
"ru":{"READY":"ГОТОВО","CONDITIONAL":"УСЛОВНО ГОТОВО","RESUBMIT":"ТРЕБУЕТСЯ ПОВТОРНАЯ ПОДАЧА"},
"kk":{"READY":"ДАЙЫН","CONDITIONAL":"ШАРТТЫ ТҮРДЕ ДАЙЫН","RESUBMIT":"ҚАЙТА ТАПСЫРУ ҚАЖЕТ"}}

TABLE_RISK = {
"en":{"SIMPLE_SAFE":"SIMPLE_SAFE","COMPLEX_SAFE_TO_PRESERVE":"COMPLEX_SAFE_TO_PRESERVE","BROKEN_REQUIRES_REVIEW":"BROKEN_REQUIRES_REVIEW"},
"ru":{"SIMPLE_SAFE":"ПРОСТАЯ / БЕЗОПАСНА ДЛЯ ОБРАБОТКИ","COMPLEX_SAFE_TO_PRESERVE":"СЛОЖНАЯ / СОХРАНИТЬ","BROKEN_REQUIRES_REVIEW":"ПОВРЕЖДЕНА / ТРЕБУЕТ ПРОВЕРКИ"},
"kk":{"SIMPLE_SAFE":"ҚАРАПАЙЫМ / ӨҢДЕУГЕ ҚАУІПСІЗ","COMPLEX_SAFE_TO_PRESERVE":"КҮРДЕЛІ / САҚТАУ ҚАЖЕТ","BROKEN_REQUIRES_REVIEW":"БҰЗЫЛҒАН / ТЕКСЕРУ ҚАЖЕТ"}}

FINDING_TITLES_RU = {
"TITLE_TEMPLATE_NONCOMPLIANT":"Титульный лист присутствует, но не соответствует шаблону",
"NORMAL_THREE_SECTION_STRUCTURE":"Структура отличается от обычной трехраздельной модели",
"SECTION_CONCLUSIONS_MISSING":"Возможно отсутствуют выводы по разделам",
"NUMERIC_CITATIONS_NO_BIBLIOGRAPHY":"Обнаружены числовые ссылки, но список литературы отсутствует",
"UNMATCHED_CITATIONS":"Ссылки без сопоставленной библиографической записи",
"DUPLICATE_REFERENCE_ENTRIES":"Возможные дубли в списке литературы",
"BROKEN_TABLE":"Таблица требует ручной проверки",
"DUPLICATE_TABLE_NUMBERS":"Повторяющиеся номера таблиц","TABLE_NUMBERING_GAPS":"Пропуски в нумерации таблиц",
"DUPLICATE_FIGURE_NUMBERS":"Повторяющиеся номера рисунков","FIGURE_NUMBERING_GAPS":"Пропуски в нумерации рисунков",
"NONEXISTENT_TABLE_REFERENCE":"Ссылка на таблицу без соответствующей подписи","NONEXISTENT_FIGURE_REFERENCE":"Ссылка на рисунок без соответствующей подписи",
"APPENDIX_REFERENCE_MISMATCH":"Несоответствие ссылок на приложения","NONEXISTENT_SECTION_REFERENCE":"Ссылка на отсутствующий раздел",
"SECTION_NUMBERING_GAPS":"Пропуски в нумерации разделов","CONTENTS_HEADING_MISMATCH":"Названия в Содержании не совпадают с заголовками",
"EMPTY_SOURCE_PLACEHOLDER":"Обнаружен пустой заполнитель источника","TABLE_PROSE_NUMERIC_INCONSISTENCY":"Числовое несоответствие между таблицей и текстом",
"DUPLICATE_PAGE_FIELDS":"Обнаружены дублирующиеся поля PAGE","AUTOMATIC_WORD_NUMBERING_DETECTED":"Обнаружена автоматическая нумерация Word",
"PAGE_FIELD_LOCATION_NONCOMPLIANT":"Номер страницы расположен в нижнем колонтитуле",
"REPEATED_METRIC_VALUE_INCONSISTENCY":"Один показатель указан с противоречащими значениями",
"PAGE_FIELD_RECHECK_REQUIRED":"Требуется повторная OOXML-проверка нумерации страниц",
"AUTOMATIC_NUMBERING_RECHECK_REQUIRED":"Требуется повторная OOXML-проверка автоматической нумерации",
"TABLE_STRUCTURE_RECHECK_REQUIRED":"Требуется повторная OOXML-проверка структуры таблиц",
"FIGURE_CAPTION_RECHECK_REQUIRED":"Требуется проверка подписей рисунков",
"STATIC_TOC_PAGE_NUMBERS_REQUIRE_UPDATE":"Требуется обновить номера страниц в Содержании",
"POST_FORMAT_CONTENT_INTEGRITY_VERIFIED":"Сохранность содержания после форматирования подтверждена"
}
FINDING_TITLES_KK = {
"TITLE_TEMPLATE_NONCOMPLIANT":"Титулдық бет бар, бірақ үлгіге сәйкес емес","NORMAL_THREE_SECTION_STRUCTURE":"Құрылым әдеттегі үш бөлімді модельден өзгеше",
"SECTION_CONCLUSIONS_MISSING":"Бөлім қорытындылары болмауы мүмкін","NUMERIC_CITATIONS_NO_BIBLIOGRAPHY":"Сандық сілтемелер бар, бірақ әдебиеттер тізімі жоқ",
"UNMATCHED_CITATIONS":"Әдебиеттер жазбасымен сәйкеспеген сілтемелер","DUPLICATE_REFERENCE_ENTRIES":"Әдебиеттер тізіміндегі ықтимал қайталанулар",
"BROKEN_TABLE":"Кесте қолмен тексеруді талап етеді","DUPLICATE_TABLE_NUMBERS":"Кесте нөмірлері қайталанады","TABLE_NUMBERING_GAPS":"Кесте нөмірлеуінде бос орындар бар",
"DUPLICATE_FIGURE_NUMBERS":"Сурет нөмірлері қайталанады","FIGURE_NUMBERING_GAPS":"Сурет нөмірлеуінде бос орындар бар",
"NONEXISTENT_TABLE_REFERENCE":"Сәйкес атауы жоқ кестеге сілтеме","NONEXISTENT_FIGURE_REFERENCE":"Сәйкес атауы жоқ суретке сілтеме",
"APPENDIX_REFERENCE_MISMATCH":"Қосымша сілтемелерінің сәйкессіздігі","NONEXISTENT_SECTION_REFERENCE":"Жоқ бөлімге сілтеме",
"SECTION_NUMBERING_GAPS":"Бөлім нөмірлеуіндегі бос орындар","CONTENTS_HEADING_MISMATCH":"Мазмұндағы атаулар нақты тақырыптармен сәйкес емес",
"EMPTY_SOURCE_PLACEHOLDER":"Бос дереккөз орны анықталды","TABLE_PROSE_NUMERIC_INCONSISTENCY":"Кесте мен мәтін арасындағы сандық сәйкессіздік",
"DUPLICATE_PAGE_FIELDS":"Қайталанатын PAGE өрістері анықталды","AUTOMATIC_WORD_NUMBERING_DETECTED":"Word автоматты нөмірлеуі анықталды",
"PAGE_FIELD_LOCATION_NONCOMPLIANT":"Бет нөмірі төменгі колонтитулда орналасқан",
"REPEATED_METRIC_VALUE_INCONSISTENCY":"Бір көрсеткіш қайшы мәндермен көрсетілген",
"PAGE_FIELD_RECHECK_REQUIRED":"Бет нөмірлеуін OOXML деңгейінде қайта тексеру қажет",
"AUTOMATIC_NUMBERING_RECHECK_REQUIRED":"Автоматты нөмірлеуді OOXML деңгейінде қайта тексеру қажет",
"TABLE_STRUCTURE_RECHECK_REQUIRED":"Кесте құрылымын OOXML деңгейінде қайта тексеру қажет",
"FIGURE_CAPTION_RECHECK_REQUIRED":"Сурет атауларын тексеру қажет",
"STATIC_TOC_PAGE_NUMBERS_REQUIRE_UPDATE":"Мазмұндағы бет нөмірлерін жаңарту қажет",
"POST_FORMAT_CONTENT_INTEGRITY_VERIFIED":"Пішімдеуден кейін мазмұнның сақталғаны расталды"
}

def rt(lang,key,**kwargs):
    d=REPORT_TEXT.get(lang,REPORT_TEXT['en']); value=d.get(key,REPORT_TEXT['en'].get(key,key)); return value.format(**kwargs)

def display_component(lang,name): return COMPONENT_NAMES.get(lang,COMPONENT_NAMES['en']).get(name,name)
def display_component_status(lang,status): return COMPONENT_STATUS.get(lang,COMPONENT_STATUS['en']).get(status,status)
def display_submission_status(lang,status): return SUBMISSION_STATUS.get(lang,SUBMISSION_STATUS['en']).get(status,status)
def display_table_risk(lang,risk): return TABLE_RISK.get(lang,TABLE_RISK['en']).get(risk,risk)
def display_finding_title(lang,code,fallback):
    if lang=='ru': return FINDING_TITLES_RU.get(code,fallback)
    if lang=='kk': return FINDING_TITLES_KK.get(code,fallback)
    return fallback
