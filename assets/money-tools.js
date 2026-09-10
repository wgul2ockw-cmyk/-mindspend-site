/* Public calculators: integer cents, no network, cookies, or storage. */
(function () {
  'use strict';
  const MAX = 1000000000;
  function cents(value) {
    const text = String(value).trim();
    if (!/^\d+(?:\.\d{1,2})?$/.test(text)) throw new Error('money');
    const n = Number(text);
    if (!Number.isFinite(n) || n > MAX) throw new Error('money');
    return Math.round(n * 100);
  }
  function whole(value, max) {
    if (!/^\d+$/.test(String(value)) || Number(value) < 1 || Number(value) > max) throw new Error('whole');
    return Number(value);
  }
  function calculate(tool, values) {
    if (tool === 'budget') {
      const income = cents(values.income);
      const fixed = cents(values.fixed), variable = cents(values.variable), saving = cents(values.saving);
      return { income, committed: fixed + variable + saving, remaining: income - fixed - variable - saving,
        needs: Math.round(income * .5), wants: Math.round(income * .3), goals: income - Math.round(income * .5) - Math.round(income * .3) };
    }
    if (tool === 'savings') {
      const remaining = Math.max(0, cents(values.target) - cents(values.saved));
      const months = whole(values.months, 1200);
      const monthly = Math.ceil(remaining / months);
      const payments = monthly ? Math.ceil(remaining / monthly) : 0;
      return { remaining, monthly, payments, final: payments ? remaining - monthly * (payments - 1) : 0 };
    }
    if (tool === 'split') {
      const bill = cents(values.bill), people = whole(values.people, 1000);
      const tipRate = Number(values.tip);
      if (!/^\d+(?:\.\d{1,2})?$/.test(String(values.tip)) || tipRate > 100) throw new Error('tip');
      const tip = Math.round(bill * tipRate / 100), total = bill + tip;
      return { total, tip, people, base: Math.floor(total / people), extra: total % people };
    }
    throw new Error('tool');
  }
  if (typeof module !== 'undefined') module.exports = { calculate, cents };
  if (typeof document === 'undefined') return;
  const th = document.documentElement.lang === 'th';
  const t = (a, b) => th ? a : b;
  document.querySelectorAll('[data-money-tool]').forEach(form => {
    form.querySelector('fieldset').disabled = false;
    const output = form.querySelector('[data-result]');
    const error = form.querySelector('[data-error]');
    const format = value => new Intl.NumberFormat(th ? 'th-TH' : 'en-US', {
      style: 'currency', currency: form.elements.currency.value, maximumFractionDigits: 2
    }).format(value / 100);
    const show = (label, value) => '<div class="result-item"><span>' + label + '</span><strong>' + format(value) + '</strong></div>';
    function update() {
      error.textContent = '';
      if (!form.checkValidity()) {
        output.replaceChildren();
        error.textContent = t('กรอกทุกช่องเป็นตัวเลขตามช่วงที่กำหนด จำนวนเงินใช้ทศนิยมได้ไม่เกิน 2 ตำแหน่ง', 'Complete every field within its range. Use at most two decimal places for money.');
        return;
      }
      try {
        const values = Object.fromEntries(new FormData(form));
        const result = calculate(form.dataset.moneyTool, values);
        let content;
        if (form.dataset.moneyTool === 'budget') {
          content = show(t('เงินที่วางไว้ในแผน', 'Allocated in your plan'), result.committed)
            + show(result.remaining < 0 ? t('แผนส่วนที่มากกว่ารายรับ', 'Plan exceeds income by') : t('ยังไม่ได้จัดสรร', 'Still unallocated'), Math.abs(result.remaining))
            + '<p>' + t('ตัวอย่างสัดส่วน 50/30/20 จากรายรับนี้: ', 'A 50/30/20 reference for this income: ')
            + [result.needs, result.wants, result.goals].map(format).join(' / ') + '</p>';
        } else if (form.dataset.moneyTool === 'savings') {
          content = show(t('ระยะห่างจากเป้าหมาย', 'Remaining to your goal'), result.remaining)
            + show(t('จำนวนต่อเดือนโดยประมาณ', 'Monthly amount'), result.monthly)
            + '<p>' + (result.remaining ? t('จำนวนงวด ', 'Number of contributions: ') + result.payments + ' · ' + t('งวดสุดท้าย ', 'Final contribution: ') + format(result.final) : t('ยอดที่กรอกถึงเป้าหมายนี้แล้ว', 'The saved amount already covers this goal.')) + '</p>';
        } else {
          content = show(t('ยอดรวมพร้อมทิปเพิ่ม', 'Total including added tip'), result.total)
            + show(t('ทิปที่เพิ่ม', 'Added tip'), result.tip);
          if (result.extra) {
            const share = (count, amount) => count + t(' คน จ่ายคนละ ', count === 1 ? ' person pays ' : ' people pay ') + format(amount);
            content += '<p>' + share(result.extra, result.base + 1) + t(' และอีก ', ' each; ') + share(result.people - result.extra, result.base) + t(' ยอดรวมจึงตรงกับบิล', ' each. These amounts add up to the exact total.') + '</p>';
          }
          else content += show(t('แต่ละคนจ่าย', 'Each person pays'), result.base);
        }
        output.innerHTML = content;
      } catch (_) {
        output.replaceChildren();
        error.textContent = t('ตรวจจำนวนเงินและจำนวนคนหรือเดือนอีกครั้ง', 'Check the amounts and the number of people or months.');
      }
    }
    form.addEventListener('submit', event => { event.preventDefault(); update(); });
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    update();
  });
})();
