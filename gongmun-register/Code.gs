/**
 * 공문 관리 대장 — Google Apps Script
 *
 * - 문서번호 자동 채번 : GC + YYMM + 월별 순번(01부터, 매월 리셋)  예) GC261001
 * - 작성일자 자동 기재 : 등록(입력) 당일 날짜
 * - 작성부서 / 작성자 : 드롭다운 선택 + 직접 입력 모두 가능 ('설정' 시트에서 목록 편집)
 * - 메뉴 [📋 공문 관리] → [✏️ 새 공문 등록] 사이드바 또는 표에 직접 입력
 */

const CFG = {
  SHEET: '공문 관리 대장',
  LIST_SHEET: '설정',
  PREFIX: 'GC',
  SEQ_DIGITS: 2,          // 순번 자릿수 (01, 02 …). 100건 이상이면 자동으로 3자리가 됩니다.
  HEADER_ROW: 7,
  FIRST_ROW: 8,
  MAX_ROWS: 1000,
  COL: { NO: 2, DOC: 3, DATE: 4, DEPT: 5, AUTHOR: 6, TO: 7, TITLE: 8, NOTE: 9 }, // B ~ I
  FIRST_COL: 2,
  LAST_COL: 9,
  HEADERS: ['No.', '문서번호', '작성일자', '작성부서', '작성자', '공문 수신처', '공문 제목', '비고'],
  DEPTS: ['글로벌사업부', '특수사업TF', '상품기획팀'],
  AUTHORS: ['최송부', '박진우', 'GURUNG RIT BAHADUR', '이진웅', '박우향', '전혁',
            '이정명', '우종민', '조민규', '김소은', '이정민'],
  COLOR: {
    navy: '#1F3A5F', navyDark: '#162B47', accent: '#2F6FED', soft: '#EEF3FB',
    band: '#F7F9FC', line: '#E3E8F0', text: '#1F2937', muted: '#6B7280',
    guideBg: '#FFFBEF', guideHead: '#F6C445', guideLine: '#F2D17A', white: '#FFFFFF'
  }
};

/* ───────────────────────── 메뉴 ───────────────────────── */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📋 공문 관리')
    .addItem('✏️ 새 공문 등록', 'showSidebar')
    .addSeparator()
    .addItem('🧾 드롭다운 목록 편집', 'openListSheet')
    .addItem('🛠 대장 초기 설정 / 서식 재적용', 'setupRegister')
    .addToUi();

  if (!SpreadsheetApp.getActive().getSheetByName(CFG.SHEET)) setupRegister();
}

function showSidebar() {
  const html = HtmlService.createHtmlOutputFromFile('Sidebar').setTitle('공문 등록');
  SpreadsheetApp.getUi().showSidebar(html);
}

function openListSheet() {
  const ss = SpreadsheetApp.getActive();
  ss.setActiveSheet(ensureListSheet_(ss));
}

/* ───────────────────────── 초기 설정 ───────────────────────── */

function setupRegister() {
  const ss = SpreadsheetApp.getActive();
  const list = ensureListSheet_(ss);
  let sh = ss.getSheetByName(CFG.SHEET);
  if (!sh) sh = ss.insertSheet(CFG.SHEET, 0);
  styleRegister_(sh, list);
  ss.setActiveSheet(sh);
  ss.toast('공문 관리 대장 설정이 완료되었습니다. (기존 데이터는 유지됩니다)', '✅ 완료', 5);
}

function ensureListSheet_(ss) {
  let sh = ss.getSheetByName(CFG.LIST_SHEET);
  if (sh) return sh;

  const C = CFG.COLOR;
  sh = ss.insertSheet(CFG.LIST_SHEET);
  const n = Math.max(CFG.DEPTS.length, CFG.AUTHORS.length);
  const rows = [];
  for (let i = 0; i < n; i++) rows.push([CFG.DEPTS[i] || '', CFG.AUTHORS[i] || '']);

  sh.getRange(1, 1, 1, 2).setValues([['작성부서', '작성자']])
    .setBackground(C.navy).setFontColor(C.white).setFontWeight('bold')
    .setHorizontalAlignment('center');
  sh.getRange(2, 1, n, 2).setValues(rows);
  sh.getRange(1, 1, 200, 2).setFontFamily('Noto Sans KR').setVerticalAlignment('middle');
  sh.setRowHeights(1, 30, 28);
  sh.setColumnWidths(1, 2, 200);
  sh.setFrozenRows(1);
  sh.getRange('D1').setValue('ℹ️ 목록에 이름을 추가·삭제하면 대장 드롭다운과 등록 창에 바로 반영됩니다.')
    .setFontColor(C.muted).setFontStyle('italic');
  sh.setTabColor('#9CA3AF');
  return sh;
}

function styleRegister_(sh, list) {
  const C = CFG.COLOR, K = CFG.COL;
  const lastCol = 14; // N
  const dataRows = CFG.MAX_ROWS - CFG.FIRST_ROW + 1;

  // 크기 확보
  if (sh.getMaxRows() < CFG.MAX_ROWS) sh.insertRowsAfter(sh.getMaxRows(), CFG.MAX_ROWS - sh.getMaxRows());
  if (sh.getMaxColumns() < lastCol) sh.insertColumnsAfter(sh.getMaxColumns(), lastCol - sh.getMaxColumns());

  // 재적용 시 기존 병합·밴딩·조건부서식 정리 (데이터는 유지)
  sh.getRange(1, 1, 6, lastCol).breakApart();
  sh.getRange(CFG.HEADER_ROW, 11, 20, 3).breakApart().clear();
  sh.getBandings().forEach(b => b.remove());
  sh.clearConditionalFormatRules();

  sh.setHiddenGridlines(true);
  sh.setTabColor(C.navy);
  sh.getRange(1, 1, sh.getMaxRows(), lastCol)
    .setFontFamily('Noto Sans KR').setFontSize(10).setFontColor(C.text).setVerticalAlignment('middle');

  // 열 너비
  sh.setColumnWidth(1, 22);
  [56, 120, 110, 130, 170, 220, 380, 160].forEach((w, i) => sh.setColumnWidth(CFG.FIRST_COL + i, w));
  sh.setColumnWidth(10, 28);
  sh.setColumnWidths(11, 3, 150);
  sh.setColumnWidth(14, 22);

  // 1~2행 : 타이틀 배너
  sh.setRowHeight(1, 56);
  sh.getRange('B1:M1').merge().setValue('📋  공문 관리 대장')
    .setFontSize(20).setFontWeight('bold').setFontColor(C.white);
  sh.getRange('A1:N1').setBackground(C.navy);
  sh.setRowHeight(2, 26);
  sh.getRange('B2:M2').merge()
    .setValue('OFFICIAL DOCUMENT REGISTER   ·   문서번호 자동 채번   ·   메뉴 [📋 공문 관리] → [✏️ 새 공문 등록]')
    .setFontSize(9).setFontColor('#C9D6EA');
  sh.getRange('A2:N2').setBackground(C.navyDark);
  sh.setRowHeight(3, 12);

  // 4~5행 : 요약 카드
  const docCol = `C${CFG.FIRST_ROW}:C`;
  const ym = `"${CFG.PREFIX}"&TEXT(TODAY(),"yymm")`;
  const cards = [
    { range: ['B4:C4', 'B5:C5'], label: '이번 달 발행', formula: `=COUNTIF(${docCol},${ym}&"*")`, fmt: '0"건"' },
    { range: ['D4:E4', 'D5:E5'], label: '누적 발행', formula: `=COUNTA(${docCol})`, fmt: '0"건"' },
    { range: ['F4:G4', 'F5:G5'], label: '다음 문서번호', accent: true,
      formula: `=${ym}&TEXT(MAX(0,ARRAYFORMULA(IF(LEFT(${docCol},6)=${ym},IFERROR(VALUE(MID(${docCol},7,9)),0),0)))+1,"${'0'.repeat(CFG.SEQ_DIGITS)}")` },
    { range: ['H4', 'H5'], label: '기준일 (오늘)', formula: '=TODAY()', fmt: 'yyyy-mm-dd (ddd)' },
    { range: ['I4', 'I5'], label: '최근 등록 번호',
      formula: `=IFERROR(INDEX(FILTER(${docCol},${docCol}<>""),COUNTA(${docCol})),"-")` }
  ];
  sh.setRowHeight(4, 24);
  sh.setRowHeight(5, 42);
  cards.forEach(c => {
    const lab = sh.getRange(c.range[0]).merge();
    const val = sh.getRange(c.range[1]).merge();
    lab.setValue(c.label).setFontSize(9).setFontColor(c.accent ? '#DCE7FF' : C.muted)
      .setBackground(c.accent ? C.accent : C.soft).setHorizontalAlignment('center');
    val.setFormula(c.formula).setFontSize(17).setFontWeight('bold')
      .setFontColor(c.accent ? C.white : C.navy)
      .setBackground(c.accent ? C.accent : C.soft).setHorizontalAlignment('center');
    if (c.fmt) val.setNumberFormat(c.fmt);
    sh.getRange(lab.getRow(), lab.getColumn(), 2, lab.getNumColumns())
      .setBorder(true, true, true, true, false, false, C.white, SpreadsheetApp.BorderStyle.SOLID_THICK);
  });
  sh.setRowHeight(6, 14);

  // 7행 : 헤더
  sh.setRowHeight(CFG.HEADER_ROW, 36);
  sh.getRange(CFG.HEADER_ROW, CFG.FIRST_COL, 1, CFG.HEADERS.length).setValues([CFG.HEADERS])
    .setBackground(C.navy).setFontColor(C.white).setFontWeight('bold')
    .setHorizontalAlignment('center');

  // 데이터 영역
  const body = sh.getRange(CFG.FIRST_ROW, CFG.FIRST_COL, dataRows, CFG.HEADERS.length);
  sh.setRowHeights(CFG.FIRST_ROW, dataRows, 30);
  body.setWrapStrategy(SpreadsheetApp.WrapStrategy.CLIP);
  sh.getRange(CFG.FIRST_ROW, K.NO, dataRows, 5).setHorizontalAlignment('center'); // No ~ 작성자
  sh.getRange(CFG.FIRST_ROW, K.TO, dataRows, 3).setHorizontalAlignment('left');
  sh.getRange(CFG.FIRST_ROW, K.NO, dataRows, 1).setFontColor(C.muted).setFontSize(9);
  sh.getRange(CFG.FIRST_ROW, K.DOC, dataRows, 1).setFontWeight('bold').setFontColor(C.navy)
    .setNumberFormat('@');
  sh.getRange(CFG.FIRST_ROW, K.DATE, dataRows, 1).setNumberFormat('yyyy-mm-dd');
  sh.getRange(CFG.FIRST_ROW, K.NOTE, dataRows, 1).setFontColor(C.muted);

  const band = sh.getRange(CFG.HEADER_ROW, CFG.FIRST_COL, dataRows + 1, CFG.HEADERS.length)
    .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, true, false);
  band.setHeaderRowColor(C.navy).setFirstRowColor(C.white).setSecondRowColor(C.band);
  body.setBorder(null, null, true, null, null, true, C.line, SpreadsheetApp.BorderStyle.SOLID);

  // 드롭다운 (목록 선택 + 직접 입력 허용)
  const deptRule = SpreadsheetApp.newDataValidation()
    .requireValueInRange(list.getRange('A2:A200'), true).setAllowInvalid(true)
    .setHelpText('목록에서 선택하거나 직접 입력하세요. (목록 편집: 설정 시트)').build();
  const authorRule = SpreadsheetApp.newDataValidation()
    .requireValueInRange(list.getRange('B2:B200'), true).setAllowInvalid(true)
    .setHelpText('목록에서 선택하거나 직접 입력하세요. (목록 편집: 설정 시트)').build();
  sh.getRange(CFG.FIRST_ROW, K.DEPT, dataRows, 1).setDataValidation(deptRule);
  sh.getRange(CFG.FIRST_ROW, K.AUTHOR, dataRows, 1).setDataValidation(authorRule);

  // 이번 달 문서 강조
  const docRange = sh.getRange(CFG.FIRST_ROW, K.DOC, dataRows, 1);
  sh.setConditionalFormatRules([
    SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied(`=LEFT($C${CFG.FIRST_ROW},6)="${CFG.PREFIX}"&TEXT(TODAY(),"yymm")`)
      .setFontColor(C.accent).setBackground(C.soft)
      .setRanges([docRange]).build()
  ]);

  // 자동 채번 영역 보호 (수정 시 경고)
  sh.getProtections(SpreadsheetApp.ProtectionType.RANGE)
    .filter(p => p.getDescription() === '자동 채번 영역')
    .forEach(p => p.remove());
  sh.getRange(CFG.FIRST_ROW, K.DOC, dataRows, 2).protect()
    .setDescription('자동 채번 영역').setWarningOnly(true);

  writeGuide_(sh);
  sh.setFrozenRows(CFG.HEADER_ROW);
}

/** 오른쪽 '문서번호 작성 요령' 안내 패널 (K~M열) */
function writeGuide_(sh) {
  const C = CFG.COLOR;
  const lines = [
    ['형식    GC + YYMM + 순번', 'bold'],
    ['• GC : 고정 접두어 (변경 불가)'],
    ['• YYMM : 작성일 기준 연도 2자리 + 월 2자리'],
    ['• 순번 : 매월 01부터 다시 시작 (월별 리셋)'],
    ['예시    2026년 10월 1번째 → GC261001', 'bold'],
    ['            2026년 10월 2번째 → GC261002'],
    ['            2026년 11월 1번째 → GC261101'],
    ['입력 방법', 'bold'],
    ['① 메뉴 [📋 공문 관리] → [✏️ 새 공문 등록] (권장)'],
    ['② 표 빈 행에 내용 입력 → 번호·일자 자동 기재'],
    ['• 부서·작성자 : 드롭다운 선택 또는 직접 입력'],
    ['⚠️ 문서번호·작성일자는 직접 수정하지 마세요'],
    ['⚠️ 취소 공문은 행 삭제 대신 비고에 \'취소\' 표기'],
    ['🔵 파란색 번호 = 이번 달 발행 문서']
  ];

  const top = CFG.HEADER_ROW;
  sh.getRange(top, 11, 1, 3).merge().setValue('📌  문서번호 작성 요령')
    .setBackground(C.guideHead).setFontColor(C.navyDark).setFontWeight('bold')
    .setHorizontalAlignment('center');
  lines.forEach((l, i) => {
    const r = sh.getRange(top + 1 + i, 11, 1, 3).merge().setValue(l[0])
      .setBackground(C.guideBg).setFontSize(9.5).setHorizontalAlignment('left')
      .setFontWeight(l[1] === 'bold' ? 'bold' : 'normal')
      .setFontColor(l[0].startsWith('⚠️') ? '#B4541A' : C.text);
    if (l[1] === 'bold') r.setFontColor(C.navy);
  });
  sh.getRange(top, 11, lines.length + 1, 3)
    .setBorder(true, true, true, true, null, null, C.guideLine, SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
}

/* ───────────────────────── 자동 채번 (표 직접 입력) ───────────────────────── */

function onEdit(e) {
  if (!e || !e.range) return;
  const sh = e.range.getSheet();
  if (sh.getName() !== CFG.SHEET) return;

  const K = CFG.COL;
  const r0 = e.range.getRow(), c0 = e.range.getColumn();
  const r1 = r0 + e.range.getNumRows() - 1, c1 = c0 + e.range.getNumColumns() - 1;
  if (r1 < CFG.FIRST_ROW || c1 < K.DEPT || c0 > K.TITLE) return;

  const start = Math.max(r0, CFG.FIRST_ROW);
  const n = r1 - start + 1;

  const lock = LockService.getDocumentLock();
  try { lock.waitLock(10000); } catch (err) { return; }
  try {
    const width = CFG.LAST_COL - CFG.FIRST_COL + 1;
    const vals = sh.getRange(start, CFG.FIRST_COL, n, width).getValues();
    const idx = c => c - CFG.FIRST_COL;
    const { prefix, dateStr } = today_();
    let seq = null;

    vals.forEach((row, i) => {
      const hasDoc = String(row[idx(K.DOC)]).trim() !== '';
      const hasInput = [K.DEPT, K.AUTHOR, K.TO, K.TITLE]
        .some(c => String(row[idx(c)]).trim() !== '');
      if (hasDoc || !hasInput) return;

      if (seq === null) seq = maxSeq_(sh, prefix);
      seq++;
      const rr = start + i;
      sh.getRange(rr, K.NO, 1, 3).setValues([[rr - CFG.HEADER_ROW, prefix + pad_(seq), dateStr]]);
    });
  } finally {
    lock.releaseLock();
  }
}

/* ───────────────────────── 사이드바용 서버 함수 ───────────────────────── */

function getSidebarData() {
  const ss = SpreadsheetApp.getActive();
  const sh = ss.getSheetByName(CFG.SHEET) || (setupRegister(), ss.getSheetByName(CFG.SHEET));
  const list = ensureListSheet_(ss);
  const { prefix, dateStr } = today_();
  const seq = maxSeq_(sh, prefix);

  const last = lastDataRow_(sh);
  const recent = [];
  if (last >= CFG.FIRST_ROW) {
    const from = Math.max(CFG.FIRST_ROW, last - 4);
    const tz = ss.getSpreadsheetTimeZone();
    sh.getRange(from, CFG.FIRST_COL, last - from + 1, CFG.LAST_COL - CFG.FIRST_COL + 1)
      .getValues().reverse().forEach(r => {
        if (!r[1]) return;
        recent.push({
          docNo: String(r[1]),
          date: r[2] instanceof Date ? Utilities.formatDate(r[2], tz, 'MM.dd') : String(r[2]).slice(5),
          dept: String(r[3]), title: String(r[6])
        });
      });
  }

  return {
    depts: columnValues_(list, 1),
    authors: columnValues_(list, 2),
    nextNo: prefix + pad_(seq + 1),
    monthCount: seq,
    today: dateStr,
    recent: recent
  };
}

function registerDocument(form) {
  const clean = v => String(v == null ? '' : v).trim();
  const data = {
    dept: clean(form.dept), author: clean(form.author),
    to: clean(form.to), title: clean(form.title), note: clean(form.note)
  };
  const missing = [['dept', '작성부서'], ['author', '작성자'], ['to', '공문 수신처'], ['title', '공문 제목']]
    .filter(([k]) => !data[k]).map(([, label]) => label);
  if (missing.length) throw new Error(missing.join(', ') + ' 을(를) 입력해 주세요.');

  const sh = SpreadsheetApp.getActive().getSheetByName(CFG.SHEET);
  if (!sh) throw new Error('대장 시트가 없습니다. 메뉴에서 [대장 초기 설정]을 먼저 실행해 주세요.');

  const lock = LockService.getDocumentLock();
  lock.waitLock(15000);
  try {
    const { prefix, dateStr } = today_();
    const docNo = prefix + pad_(maxSeq_(sh, prefix) + 1);
    const row = lastDataRow_(sh) + 1;
    if (row > sh.getMaxRows()) sh.insertRowsAfter(sh.getMaxRows(), 200);

    sh.getRange(row, CFG.FIRST_COL, 1, CFG.HEADERS.length).setValues([[
      row - CFG.HEADER_ROW, docNo, dateStr, data.dept, data.author, data.to, data.title, data.note
    ]]);
    SpreadsheetApp.flush();
    sh.getRange(row, CFG.FIRST_COL, 1, CFG.HEADERS.length).activate();
    return { docNo: docNo, date: dateStr, row: row };
  } finally {
    lock.releaseLock();
  }
}

/* ───────────────────────── 유틸 ───────────────────────── */

function today_() {
  const tz = SpreadsheetApp.getActive().getSpreadsheetTimeZone() || 'Asia/Seoul';
  const now = new Date();
  return {
    prefix: CFG.PREFIX + Utilities.formatDate(now, tz, 'yyMM'),
    dateStr: Utilities.formatDate(now, tz, 'yyyy-MM-dd')
  };
}

/** 해당 월(prefix = GCYYMM)에서 사용된 가장 큰 순번 */
function maxSeq_(sh, prefix) {
  const last = lastDataRow_(sh);
  if (last < CFG.FIRST_ROW) return 0;
  return sh.getRange(CFG.FIRST_ROW, CFG.COL.DOC, last - CFG.FIRST_ROW + 1, 1).getValues()
    .reduce((max, [v]) => {
      const s = String(v).trim();
      if (!s.startsWith(prefix)) return max;
      const n = parseInt(s.slice(prefix.length), 10);
      return isNaN(n) ? max : Math.max(max, n);
    }, 0);
}

/** B~I열 기준 마지막 데이터 행 (안내 패널·요약 카드는 제외) */
function lastDataRow_(sh) {
  const maxRow = sh.getLastRow();
  if (maxRow < CFG.FIRST_ROW) return CFG.FIRST_ROW - 1;
  const vals = sh.getRange(CFG.FIRST_ROW, CFG.FIRST_COL, maxRow - CFG.FIRST_ROW + 1,
    CFG.LAST_COL - CFG.FIRST_COL + 1).getValues();
  for (let i = vals.length - 1; i >= 0; i--) {
    // No.(B열)만 있는 행은 빈 행으로 간주
    if (vals[i].slice(1).some(v => String(v).trim() !== '')) return CFG.FIRST_ROW + i;
  }
  return CFG.FIRST_ROW - 1;
}

function columnValues_(sh, col) {
  const last = sh.getLastRow();
  if (last < 2) return [];
  return sh.getRange(2, col, last - 1, 1).getValues()
    .map(r => String(r[0]).trim()).filter(Boolean);
}

function pad_(n) {
  return String(n).padStart(CFG.SEQ_DIGITS, '0');
}
