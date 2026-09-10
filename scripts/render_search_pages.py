#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bilingual, crawlable money tools and a receipt workflow guide. No runtime translation."""
from pathlib import Path
import html
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
DATE = '2026-09-10'
ROUTES = {
    'budget': ('monthly-budget-planner.html', 'monthly-budget-planner-th.html'),
    'savings': ('savings-goal-calculator.html', 'savings-goal-calculator-th.html'),
    'split': ('split-bill-calculator.html', 'split-bill-calculator-th.html'),
    'receipt': ('receipt-scanner.html', 'receipt-scanner-th.html'),
}

def content(kind, th):
    def t(a, b): return a if th else b
    if kind == 'budget':
        return t('เครื่องคำนวณงบรายเดือนฟรี', 'Free monthly budget planner'), t(
            'ลองวางรายรับ ค่าใช้จ่าย และเงินออมในแผนเดียวกัน เครื่องคำนวณงบรายเดือนนี้แสดงเงินที่ยังไม่ได้จัดสรร พร้อมตัวอย่าง 50/30/20 ใช้ได้ฟรีโดยไม่ต้องสมัครบัญชี',
            'Build a monthly budget from your take-home income, bills, everyday expenses, and savings. This free budget planner shows what is still unallocated and a 50/30/20 reference. No account needed.'), [
            ('how', t('เริ่มจากเงินที่ใช้ได้จริงในเดือนนี้', 'How to make a monthly budget'), t('''
<p>รายรับในเครื่องมือนี้คือเงินหลังหักภาษีและรายการที่ถูกหักก่อนเข้าบัญชีแล้ว ถ้ารายรับแต่ละเดือนไม่เท่ากัน ใช้ยอดที่ยืนยันได้ก่อน แล้วลองคำนวณใหม่เมื่อยอดเปลี่ยน ไม่จำเป็นต้องเดารายรับที่ยังมาไม่ถึง</p>
<ol><li>รวมค่าใช้จ่ายประจำ เช่น ค่าเช่า อินเทอร์เน็ต และยอดชำระหนี้ที่อยู่ในแผนเดือนนี้</li><li>ใส่ยอดที่คาดว่าจะใช้กับอาหาร เดินทาง และค่าใช้จ่ายที่เปลี่ยนไปในแต่ละวัน</li><li>ใส่เงินที่ตั้งใจแยกไว้สำหรับเป้าหมาย โดยไม่รวมยอดเดียวกันซ้ำในค่าใช้จ่าย</li><li>อ่านยอดที่ยังไม่ได้จัดสรร หากแผนมากกว่ารายรับ ตัวเลขจะแสดงส่วนต่างเพื่อกลับมาดูสมมติฐาน</li></ol>
<p>งบประมาณเป็นภาพก่อนใช้เงิน ส่วนบันทึกรายจ่ายเป็นภาพที่เกิดขึ้นจริง การดูสองภาพคู่กันช่วยให้เห็นว่าหมวดไหนยังขาดรายการ หรือเดือนนี้มีเหตุการณ์ที่ไม่ได้อยู่ในแผน</p>''', '''
<p>Use income after tax and payroll deductions, rather than your headline salary. If income changes from month to month, start with money you can reasonably confirm and rerun the plan when it changes.</p>
<ol><li>Add fixed commitments such as rent, internet, and scheduled debt payments.</li><li>Estimate variable expenses such as groceries, transport, and meals.</li><li>Enter the amount you plan to set aside for savings, without counting it again in expenses.</li><li>Read the unallocated balance. If the plan exceeds income, the calculator shows the size of that gap.</li></ol>
<p>A budget describes what you expect; an expense tracker records what actually happened. Comparing the two can reveal a missing bill or an assumption that no longer fits your routine.</p>''')),
            ('example', t('ตัวอย่างงบเดือนหนึ่ง', 'A monthly budget example'), t('''
<p>ตัวเลขตัวอย่าง: รายรับ 32,000 บาท ค่าใช้จ่ายประจำ 12,000 บาท ค่าใช้จ่ายแปรผัน 8,000 บาท และเงินออม 4,000 บาท รวมแผน 24,000 บาท จึงยังไม่ได้จัดสรร 8,000 บาท ตัวเลขนี้ไม่ได้แปลว่าใช้เพิ่มได้ทั้งหมด เพราะอาจยังมีบิลหรือภาระที่ไม่ได้กรอก</p>
<p>ค่าใช้จ่ายรายปี เช่น ประกันหรือค่าบริการบางรายการ อาจถูกมองข้ามในเดือนปกติ จะใส่ในเดือนที่จ่ายจริง หรือกันยอดรายปีหาร 12 ไว้แต่ละเดือนก็ได้ เลือกวิธีเดียวเพื่อไม่ให้ยอดซ้ำ</p>''', '''
<p>Illustration: 32,000 income minus 12,000 fixed bills, 8,000 variable spending, and 4,000 savings leaves 8,000 unallocated. That amount is not automatically available for extra purchases: the calculation only knows the commitments you entered.</p>
<p>Annual insurance and irregular bills can disappear from an ordinary monthly view. You can place a bill in its payment month or reserve its annual total divided by 12. Use one approach consistently so you do not count both as new spending.</p>''')),
            ('rule', t('50/30/20 เป็นจุดเริ่ม ไม่ใช่เกณฑ์ตัดสิน', 'What does the 50/30/20 budget rule mean?'), t('''
<p>ตัวอย่างนี้แบ่งรายรับหลังหักรายการเป็น 50% สำหรับสิ่งจำเป็น 30% สำหรับสิ่งที่เลือกใช้ และ 20% สำหรับเงินออมกับการชำระหนี้เพิ่มเติม รายรับ 32,000 บาทจะแบ่งได้ 16,000 / 9,600 / 6,400 บาท</p>
<p>สัดส่วนนี้เป็นเพียงแนวอ้างอิง ค่าเช่า ภาระครอบครัว หรือรายรับไม่สม่ำเสมออาจทำให้สัดส่วนอื่นเหมาะกับชีวิตมากกว่า เครื่องมือแสดงตัวอย่างนี้แยกจากแผนที่กรอก และไม่ให้คะแนนว่าใช้เงินถูกหรือผิด</p>
<p><a href="https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/teach/activities/analyzing-budgets/">อ่านกิจกรรมเรื่องสัดส่วนงบประมาณจาก CFPB</a></p>''', '''
<p>The reference divides take-home income into 50% for needs, 30% for wants, and 20% for savings and additional debt repayment. On 32,000, that is 16,000 / 9,600 / 6,400. It is a starting framework, not a universal target.</p>
<p>Housing costs, family commitments, and variable income can make a different split more realistic. The reference does not change your entered plan or grade your spending. <a href="https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/teach/activities/analyzing-budgets/">CFPB provides an introductory budget exercise</a> using this framework.</p>''')),
            ('next', t('จากแผนไปสู่รายการจริง', 'Turn your plan into a daily record'), t('''
<p>ดาวน์โหลด <a href="./budget-tracker-free-th.html">ตารางรายรับรายจ่ายฟรี</a> เพื่อจดแผนและยอดจริงแยกกัน หรือดู <a href="./#feat">วิธีบันทึกใน MindSpend</a> ที่มีมุมมองวางแผนกับฉับพลัน บิลที่วางแผนไว้อาจมีจำนวนเปลี่ยนได้ และรายการฉับพลันก็ไม่ได้แปลว่าเป็นรายการที่ไม่จำเป็น</p>''', '''
<p>Use the <a href="./free-budget-tracker.html">free budget and expense worksheets</a> to keep planned and actual amounts side by side. For a phone-based record, explore <a href="./en.html#feat">MindSpend’s iPhone expense tracker</a> and its planned-versus-impulse view. A planned purchase can still change in price, and an impulse decision is not automatically unnecessary.</p>''')),
        ]
    if kind == 'savings':
        return t('เครื่องคำนวณเป้าหมายเงินออมฟรี', 'Free savings goal calculator'), t(
            'ใส่เป้าหมาย ยอดที่แยกไว้แล้ว และจำนวนเดือน เพื่อเห็นยอดออมต่อเดือน เครื่องมือนี้คิดจากเงินที่เติมเข้าไปเท่านั้น ไม่รวมดอกเบี้ยหรือผลตอบแทนลงทุน',
            'Work out how much to save each month from a target, your current savings, and the time available. This free savings goal calculator uses contributions only, with no assumed interest or investment return.'), [
            ('how', t('เป้าหมาย ยอดปัจจุบัน และเวลา', 'How the savings goal calculator works'), t('''
<p>เริ่มจากเป้าหมายเดียว เช่น เงินสำหรับคอร์สเรียน ทริป หรือค่าใช้จ่ายที่รู้ว่าจะเกิด ใส่เฉพาะเงินที่แยกไว้เพื่อเป้าหมายนี้จริง ๆ ไม่รวมเงินในบัญชีที่ต้องใช้จ่ายรายการอื่น และไม่ใช้ยอดเดียวกันรองรับหลายเป้าหมายพร้อมกัน</p>
<p>สูตรคือ <strong>(เป้าหมาย − เงินที่มีแล้ว) ÷ จำนวนเดือน</strong> ถ้าเงินที่มีครอบคลุมเป้าหมายแล้ว ยอดที่ยังต้องเติมจะเป็นศูนย์ ระบบปัดยอดรายเดือนขึ้นเป็นสตางค์ และแสดงงวดสุดท้ายที่อาจน้อยลงเพื่อไม่ให้เกินเป้าหมาย</p>''', '''
<p>Choose one goal: a course, a trip, or an upcoming purchase. Enter only money already set aside for this goal. A bank balance also needed for rent is not all available savings, and the same money should not fund two goals at once.</p>
<p>The formula is <strong>(target − current savings) ÷ months</strong>. If your current savings already cover the target, the remaining amount is zero. The calculator rounds the monthly contribution up to the nearest cent and shows a smaller final contribution when needed.</p>''')),
            ('example', t('ตัวอย่าง: เป้าหมาย 30,000 บาท', 'Example: a 30,000 savings target'), t('''
<p>หากต้องการ 30,000 บาท มีแล้ว 6,000 บาท และเหลือเวลา 12 เดือน ระยะห่างคือ 24,000 บาท หรือเดือนละ 2,000 บาท ถ้าเพิ่มเวลาเป็น 24 เดือน จำนวนต่อเดือนจะเป็น 1,000 บาท ทั้งสองแบบคิดจากเงินเติมจริงโดยไม่สมมติผลตอบแทน</p>
<p>กรณีเหลือเพียง 100 บาทใน 3 เดือน ระบบจะแสดงงวดละ 33.34 บาท และงวดสุดท้าย 33.32 บาท เพื่อให้รวมกันเท่ากับ 100 บาทพอดี ตัวเลขทุกตัวในตัวอย่างเป็นสมมติฐาน ไม่ใช่ข้อมูลผู้ใช้</p>''', '''
<p>A target of 30,000, with 6,000 already saved and 12 months available, leaves 24,000 to fund: 2,000 per month. Extending the time to 24 months changes the contribution to 1,000 per month. Neither scenario assumes returns.</p>
<p>For 100 remaining over three months, the result is 33.34 per month with a final contribution of 33.32. This keeps the total at exactly 100. All example amounts are illustrative, not customer data.</p>''')),
            ('fit', t('ดูเป้าหมายร่วมกับงบรายเดือน', 'Does the contribution fit your monthly budget?'), t('''
<p>นำยอดต่อเดือนไปใส่ใน <a href="./monthly-budget-planner-th.html">เครื่องวางแผนงบรายเดือน</a> เพื่อดูร่วมกับค่าใช้จ่ายจริง หากยอดยังไม่ลงตัว ลองเปลี่ยนจำนวนเงินเป้าหมายหรือเวลา แล้วดูว่าสมมติฐานไหนใกล้ชีวิตตอนนี้มากกว่า</p>
<p>เครื่องมือนี้ไม่รวมค่าธรรมเนียม ภาษี เงินเฟ้อ หรือการเปลี่ยนแปลงของมูลค่าลงทุน การเห็นจำนวนต่อเดือนไม่ได้ยืนยันว่าจำนวนดังกล่าวเหมาะกับภาระทั้งหมดของเธอ</p>''', '''
<p>Put the monthly amount into the <a href="./monthly-budget-planner.html">monthly budget planner</a> alongside bills and everyday expenses. If the amounts do not fit together, compare a different deadline or target and inspect which assumption changed.</p>
<p>This tool does not model fees, tax, inflation, or investment value changes. A monthly contribution is arithmetic, not a claim that it is affordable in your circumstances. Money needed for scheduled bills remains a separate commitment.</p>''')),
            ('track', t('เครื่องคำนวณต่างจากตัวติดตามเงินออมอย่างไร', 'Savings calculator vs. savings goal tracker'), t('''
<p>เครื่องคำนวณช่วยเห็นแผน ส่วนตัวติดตามเป้าหมายบันทึกเงินที่เติมจริง <a href="./#feat">MindSpend มีเป้าหมายเงินออมในแอป iPhone</a> เพื่อดูยอดที่เพิ่มเข้าไปตามการบันทึก การกดคำนวณบนหน้านี้ไม่เปิดบัญชี ไม่โอนเงิน และไม่อัปเดตข้อมูลในแอป</p>
<p>สามารถคัดยอดไปเก็บในตารางของตัวเองแล้วกลับมาคำนวณใหม่เมื่อมีเงินเติมหรือเวลาที่เหลือเปลี่ยน ยอดในเบราว์เซอร์ไม่ถูกบันทึกถาวรและจะเริ่มจากตัวอย่างเมื่อโหลดหน้าใหม่</p>''', '''
<p>A calculator describes a plan. A savings goal tracker records actual contributions. <a href="./en.html#feat">MindSpend includes savings goals in its iPhone app</a>, where recorded contributions can show progress. Calculating here does not open an account, move money, or update the app.</p>
<p>Copy the result to your own worksheet and rerun it when your saved amount or deadline changes. This page does not retain entries after a reload; it starts again with the labelled example.</p>''')),
        ]
    if kind == 'split':
        return t('เครื่องหารบิลและคำนวณทิปฟรี', 'Free split bill & tip calculator'), t(
            'หารค่าอาหารหรือค่าใช้จ่ายที่ทุกคนตกลงจ่ายเท่ากัน ใส่ยอดบิล จำนวนคน และทิปที่ต้องการเพิ่ม ระบบจัดเศษสตางค์ให้ยอดรวมตรงกับบิล ไม่ต้องสมัครบัญชี',
            'Split a restaurant bill or another shared expense equally. Enter the bill, number of people, and any extra tip. The calculator distributes leftover cents so everyone’s amounts add up to the exact total.'), [
            ('how', t('ใส่ยอดที่พร้อมหาร', 'How to split a bill equally'), t('''
<ol><li>ใส่ยอดบิลที่รวมภาษีและค่าบริการซึ่งร้านคิดมาแล้ว</li><li>ใส่จำนวนคนที่ตกลงแชร์ยอดนี้ จำนวนต้องเป็นจำนวนเต็มอย่างน้อยหนึ่งคน</li><li>หากมีทิปเพิ่ม ให้ใส่เปอร์เซ็นต์จากยอดบิลที่กรอก ถ้ารวมทิปไว้แล้ว ให้ใช้ 0 เพื่อไม่คิดซ้ำ</li></ol>
<p>เครื่องมือนี้หารเท่ากันตามจำนวนคน เหมาะเมื่อทุกคนตกลงแชร์ยอดเดียวกัน ถ้าบางคนสั่งมากกว่า จ่ายเฉพาะบางรายการ หรือมีผู้จ่ายล่วงหน้าหลายคน จำเป็นต้องแยกรายการก่อน</p>''', '''
<ol><li>Enter the final bill including any tax and service charge already added by the restaurant.</li><li>Enter the number of people sharing that amount. Use a whole number of at least one.</li><li>Add an optional tip percentage, calculated on the bill amount you entered. If the bill already includes your tip, leave this at zero.</li></ol>
<p>This is an equal split. It fits a group that has agreed to share the same total. Different orders, partial participation, or several people paying in advance need an item-level record instead.</p>''')),
            ('rounding', t('ทำไมบางคนต่างกัน 1 สตางค์', 'Why one person may pay a cent more'), t('''
<p>ตัวอย่าง 1,000 บาทหาร 3 คน หารได้ 333.333… บาท แต่จ่ายได้เป็นหน่วยสตางค์ ระบบจึงแบ่งเป็น 333.34 บาทหนึ่งคน และ 333.33 บาทสองคน รวมเท่ากับ 1,000 บาท ถ้าปัดทุกคนขึ้นจะเกินบิล และถ้าปัดลงทุกคนจะขาด</p>
<p>ส่วนทิปจะปัดเป็นสตางค์ก่อน แล้วจึงนำไปหารรวมกับยอดบิล กลุ่มสามารถตกลงเองว่าใครรับเศษที่ต่างกัน เครื่องมือไม่ได้กำหนดชื่อผู้จ่าย</p>''', '''
<p>For a 1,000 bill shared by three people, the exact division is 333.333… . One person pays 333.34 and two pay 333.33. Together those amounts equal 1,000. Rounding everyone up would collect too much; rounding everyone down would leave a shortfall.</p>
<p>The added tip is first rounded to cents, then included in the total before splitting. Your group can decide who covers an extra cent; the calculator does not assign names or choose a payer.</p>''')),
            ('example', t('ตัวอย่างบิลพร้อมทิป', 'Example with an optional tip'), t('''
<p>ยอดบิล 1,200 บาท ทิปเพิ่ม 10% คือ 120 บาท ยอดรวม 1,320 บาท หาร 4 คนเท่ากับคนละ 330 บาท เปอร์เซ็นต์นี้เป็นเพียงตัวอย่างสำหรับอธิบายสูตร ไม่ใช่อัตราที่ต้องจ่าย</p>
<p>ใช้สกุลเงินเดียวตลอดบิล ตัวเลือกสกุลเงินเปลี่ยนรูปแบบการแสดงผลเท่านั้น ไม่แปลงอัตราแลกเปลี่ยน หากทริปใช้หลายสกุลเงิน ให้ตกลงยอดที่แปลงแล้วก่อนนำมาหาร</p>''', '''
<p>A 1,200 bill with a 10% added tip produces a 120 tip and a 1,320 total. Four people pay 330 each. The percentage is an arithmetic example, not a recommended tipping rate.</p>
<p>Use one currency per calculation. Changing the currency selector changes formatting only; it does not convert exchange rates. For a trip with several currencies, agree on converted amounts before combining them.</p>''')),
            ('app', t('ถ้าต้องแบ่งตามรายการในใบเสร็จ', 'When you need item-by-item expense splitting'), t('''
<p>ใน <a href="./#feat">MindSpend กลุ่มและบิลแบ่ง</a> ใช้บันทึกสมาชิกและจัดสรรรายการในใบเสร็จ เหมาะกับการเก็บรายละเอียดว่ารายการไหนเกี่ยวกับใครบ้าง ส่วนเครื่องมือบนเว็บนี้ตอบโจทย์บิลเดียวที่หารเท่ากัน</p>
<p>กลุ่มในแอปเป็นข้อมูลที่จัดการบนเครื่อง การแนบสลิปหรือเปลี่ยนสถานะจ่ายแล้วเป็นการบันทึกหลักฐาน ไม่ใช่การโอนเงินหรือการยืนยันยอดจากธนาคาร <a href="./receipt-scanner-th.html">อ่านขั้นตอนตรวจใบเสร็จก่อนบันทึก</a> และ <a href="./budget-tracker-free-th.html">บันทึกเฉพาะส่วนค่าใช้จ่ายของตัวเอง</a> เพื่อไม่ให้ยอดทั้งกลุ่มถูกนับเป็นรายจ่ายของคนเดียว</p>''', '''
<p><a href="./en.html#feat">MindSpend’s groups and shared bills</a> keep member and receipt-item details in the iPhone app. That is useful when different people share different items. The free browser tool here handles one bill split equally.</p>
<p>Groups in the app are managed locally. Attaching a receipt or marking an amount paid records evidence; it does not transfer money or confirm settlement with a bank. See the <a href="./receipt-scanner.html">receipt review workflow</a>, and <a href="./free-budget-tracker.html">track your own expense share</a> so the entire group bill does not become your personal spending.</p>''')),
        ]
    return t('สแกนสลิปและใบเสร็จ เพื่อบันทึกรายจ่าย', 'Receipt & payment slip scanning for expense tracking'), t(
        'เปลี่ยนภาพสลิปหรือใบเสร็จเป็นร่างรายการที่ตรวจได้ใน MindSpend สำหรับ iPhone ดูความต่างของสลิปโอนเงินกับใบเสร็จ ข้อมูลที่ต้องตรวจ และวิธีไม่ให้รายจ่ายซ้ำ',
        'MindSpend for iPhone can turn a receipt or Thai payment slip into a reviewable expense draft. Learn what to check, how the two documents differ, and how to avoid duplicate entries.'), [
        ('difference', t('สลิปโอนเงินกับใบเสร็จให้ข้อมูลต่างกัน', 'Receipt scanner vs. payment slip reader'), t('''
<p>ใบเสร็จจากร้านอาจมีรายการสินค้า จำนวน ส่วนลด ภาษี และยอดรวม ส่วนสลิปโอนเงินอาจมีผู้ส่ง ผู้รับ จำนวนเงิน วันเวลา และเลขอ้างอิง สลิปแสดงเหตุการณ์ชำระเงิน แต่ไม่จำเป็นต้องบอกว่าซื้อสินค้าอะไรบ้าง</p>
<p>การอ่านภาพช่วยลดงานพิมพ์ได้ แต่ตัวเลขที่อ่านออกมาไม่ใช่การตรวจสอบกับธนาคาร ภาพที่มี QR หรือเลขอ้างอิงก็ไม่ได้ยืนยันด้วยตัวมันเองว่าเอกสารเป็นของจริงหรือผู้รับได้รับเงินแล้ว</p>''', '''
<p>A shop receipt can list products, quantities, discounts, tax, and a total. A Thai payment slip may show sender, recipient, amount, time, and a reference. A slip records a payment event but does not necessarily identify every item purchased.</p>
<p>Image reading can reduce typing. Extracting an amount is not the same as checking it against a bank. A QR code or reference number in an image does not, by itself, establish document authenticity or confirm that someone received money.</p>''')),
        ('workflow', t('จากภาพไปสู่รายการที่ตรวจแล้ว', 'A review-first receipt scanning workflow'), t('''
<ol><li><strong>เลือกภาพที่อ่านได้</strong> ใช้ภาพเต็มที่ไม่ตัดยอดรวม วันเวลา หรือชื่อร้านออก ระวังภาพเบลอและแสงสะท้อน</li><li><strong>เปิดขั้นตอนอ่านภาพในแอป</strong> ใช้เมนูบันทึกของ MindSpend และดูรายละเอียดสิทธิ์หรือสติ+ ที่แสดงในเวอร์ชันที่ใช้อยู่</li><li><strong>ตรวจร่างรายการ</strong> เทียบยอดเงิน วัน ร้าน และกระเป๋ากับภาพต้นฉบับก่อนบันทึก อย่าเดาส่วนที่มองไม่เห็น</li><li><strong>เชื่อมกับบริบท</strong> เลือกหมวดและวางแผนหรือฉับพลันตามตอนที่ตัดสินใจซื้อ สลิปไม่ได้บอกความตั้งใจแทนเรา</li></ol>
<p>หากภาพหนึ่งมีรายการสินค้าหลายอย่าง การบันทึกเป็นยอดเดียวกับการแยกรายการจะให้รายละเอียดต่างกัน เลือกแบบที่ต้องการก่อนบันทึก แล้วตรวจว่ายอดย่อยรวมตรงกับใบเสร็จ</p>''', '''
<ol><li><strong>Choose a readable image.</strong> Keep the total, date, and merchant visible. Blur, glare, and cropping can remove the information needed for a reliable draft.</li><li><strong>Open the image-reading workflow in the app.</strong> Use MindSpend’s logging menu and review any permission or Sati+ requirement shown in your installed version.</li><li><strong>Check the draft.</strong> Compare amount, date, merchant, and wallet with the original before saving. Do not guess missing digits.</li><li><strong>Add the context.</strong> Select the category and planned or impulse tag from the purchase decision. A receipt cannot determine your intention.</li></ol>
<p>A single total and an itemized record provide different levels of detail. Choose the record you want, then confirm that item amounts and adjustments reconcile with the receipt.</p>''')),
        ('duplicate', t('จ่ายครั้งเดียว แต่มีหลักฐานสองใบ', 'Avoid recording one purchase twice'), t('''
<p>ตัวอย่าง: ซื้ออาหาร 250 บาทและมีทั้งใบเสร็จร้านกับสลิปโอน 250 บาท ถ้าทั้งสองภาพเป็นการจ่ายครั้งเดียว การบันทึกเป็นรายจ่ายสองรายการจะกลายเป็น 500 บาท ก่อนเพิ่มรายการ ให้ดูวันที่ ยอดเงิน ร้าน และบันทึกเดิมร่วมกัน</p>
<p>แต่ยอดเงินและวันที่เหมือนกันก็ไม่ได้แปลว่าซ้ำเสมอไป เช่น ซื้อกาแฟสองครั้งราคาเท่ากัน ระบบหรือคนอ่านจึงควรมีหลักฐานมากกว่ายอดที่ตรงกัน อย่าลบรายการเพียงเพราะจำนวนเงินเหมือนกัน</p>''', '''
<p>Example: lunch costs 250 and you have both a shop receipt and a 250 payment slip for that purchase. Recording both as separate expenses would report 500. Compare the date, amount, merchant, and existing records before adding another entry.</p>
<p>Matching amounts and dates alone do not prove duplication. Two separate coffees can cost the same on the same day. Keep the original evidence and resolve the specific transaction rather than deleting a record solely because its number matches.</p>''')),
        ('privacy', t('ข้อมูลในภาพและขอบเขตฟีเจอร์', 'Privacy, permissions, and free-feature boundaries'), t('''
<p>สลิปอาจมีชื่อหรือข้อมูลบัญชีส่วนบุคคล เว็บหน้านี้เป็นคู่มือและไม่มีช่องอัปโหลดภาพ การอ่านภาพในแอปอาจใช้บริการ AI ภายนอกสำหรับรายการที่ผู้ใช้เลือกส่ง หลังให้ความยินยอมแยกต่างหาก จึงไม่ควรเข้าใจว่าการอ่านภาพทุกแบบทำงานออฟไลน์ทั้งหมด</p>
<p>การบันทึกเองเป็นส่วนพื้นฐานฟรี ส่วนเครื่องมือนำเข้าหรือทำงานอัตโนมัติบางอย่างอยู่ในสติ+ ตรวจ <a href="./faq.html#sati">รายละเอียดสิทธิ์ปัจจุบัน</a> และ <a href="./privacy.html">นโยบายความเป็นส่วนตัว</a> ก่อนเลือกใช้</p>
<p><a href="./support.html#contact">ติดต่อทีมเพื่อช่องทางดาวน์โหลด MindSpend ที่ใช้บน iPhone</a> หน้านี้ไม่ได้ให้บริการบัญชีธุรกิจหรือรับรองเอกสารเพื่อการยื่นภาษี</p>''', '''
<p>Payment slips can include names or account information. This webpage is a guide and has no image upload. In the app, an image-reading workflow may send the material you select to an external AI service after separate consent. Do not assume every scanning feature works entirely offline.</p>
<p>Manual expense recording belongs to the free core; some import and automation tools are part of Sati+. Check the <a href="./faq.html#sati">current feature boundaries (Thai)</a> and <a href="./privacy.html">bilingual privacy policy</a> before choosing a workflow.</p>
<p><a href="./support.html#contact">Contact the MindSpend team for the official iPhone download channel.</a> This guide does not offer business bookkeeping or certify receipts for tax filing.</p>''')),
    ]

def form(kind, th):
    if kind == 'receipt': return ''
    def t(a, b): return a if th else b
    definitions = {
        'budget': [('income', t('รายรับหลังหักรายการ / เดือน', 'Monthly take-home income'), 32000), ('fixed', t('ค่าใช้จ่ายประจำ / เดือน', 'Monthly fixed commitments'), 12000), ('variable', t('ค่าใช้จ่ายแปรผัน / เดือน', 'Monthly variable expenses'), 8000), ('saving', t('เงินออมที่วางแผน / เดือน', 'Planned monthly savings'), 4000)],
        'savings': [('target', t('จำนวนเงินเป้าหมาย', 'Target amount'), 30000), ('saved', t('เงินที่แยกไว้แล้ว', 'Already set aside'), 6000), ('months', t('จำนวนเดือนที่เหลือ', 'Months available'), 12)],
        'split': [('bill', t('ยอดบิลก่อนทิปที่ต้องการเพิ่ม', 'Bill before any added tip'), 1000), ('people', t('จำนวนคน', 'Number of people'), 3), ('tip', t('ทิปเพิ่ม (%)', 'Extra tip (%)'), 0)],
    }
    fields = ''
    for name, label, default in definitions[kind]:
        integer = name in ('months','people')
        maximum = 1200 if name == 'months' else 1000 if name == 'people' else 100 if name == 'tip' else 1000000000
        fields += f'<label for="{name}">{label}<input id="{name}" name="{name}" type="number" inputmode="{"numeric" if integer else "decimal"}" min="{1 if integer else 0}" max="{maximum}" step="{1 if integer else "0.01"}" value="{default}" required></label>'
    return f'''<form class="tool-panel" data-money-tool="{kind}" aria-label="{t('เครื่องคำนวณฟรี','Free calculator')}">
<h2>{t('ลองใส่ตัวเลขของเธอ','Try your own numbers')}</h2><p class="tool-hint">{t('เริ่มด้วยตัวเลขตัวอย่าง เปลี่ยนเป็นยอดของตัวเองได้ ตัวเลือกสกุลเงินไม่แปลงอัตราแลกเปลี่ยน','Starts with example amounts. Replace them with your own. Currency selection changes formatting, not exchange rates.')}</p>
<noscript><p>{t('เครื่องคำนวณต้องใช้ JavaScript อ่านสูตรและตัวอย่างด้านล่าง หรือใช้ตาราง CSV ได้โดยไม่เปิด JavaScript','The calculator needs JavaScript. The formulas and examples below, and the CSV worksheets, remain available without it.')}</p></noscript>
<fieldset disabled><legend>{t('ข้อมูลสำหรับคำนวณ','Calculation inputs')}</legend><div class="tool-fields">{fields}<label for="currency">{t('สกุลเงิน','Currency')}<select name="currency" id="currency"><option value="THB">THB · ฿</option><option value="USD">USD · $</option><option value="EUR">EUR · €</option><option value="GBP">GBP · £</option></select></label></div>
<button class="button" type="submit">{t('คำนวณ','Calculate')}</button></fieldset><p class="tool-error" data-error role="alert"></p><div class="tool-result" data-result role="status" aria-live="polite" aria-atomic="true"></div>
<p class="tool-hint">{t('คำนวณในเบราว์เซอร์ ไม่มีการส่งหรือบันทึกค่าที่กรอก โหลดหน้าใหม่แล้วเริ่มจากตัวอย่างอีกครั้ง','Calculated in your browser. Your entries are not sent or saved. Reloading restores the example amounts.')}</p></form>'''

def render(kind, lang):
    th = lang == 'th'
    def t(a, b): return a if th else b
    filename = ROUTES[kind][1 if th else 0]
    alternate = ROUTES[kind][0 if th else 1]
    home = './' if th else './en.html'
    tracker = 'budget-tracker-free-th.html' if th else 'free-budget-tracker.html'
    title, intro, sections = content(kind, th)
    toc = ''.join(f'<li><a href="#{key}">{heading}</a></li>' for key, heading, _ in sections)
    body = ''.join(f'<section id="{key}"><h2>{heading}</h2>{text}</section>' for key, heading, text in sections)
    related = [(tracker, t('ตารางบันทึกรายจ่ายฟรี','Free expense tracker worksheets'))] + [(paths[1 if th else 0], content(key, th)[0]) for key, paths in ROUTES.items() if key != kind]
    cards = ''.join(f'<a href="./{url}"><strong>{label}</strong></a>' for url,label in related)
    source = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- SEO:START --><!-- SEO:END -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@400;500;600;700&amp;family=Chonburi&amp;family=Space+Mono:wght@400;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/guides.css"><link rel="stylesheet" href="./assets/money-tools.css"><script src="./assets/money-tools.js" defer></script></head>
<body class="tool-page"><a class="skip" href="#main">{t('ข้ามไปเนื้อหา','Skip to content')}</a>
<nav class="guide-nav" aria-label="{t('เมนูหลัก','Main navigation')}"><a class="brand" href="{home}"><img src="./assets/icons/favicon-48.png" alt="" width="38" height="38">MindSpend</a><div class="links"><a href="./{tracker}">{t('บันทึกรายจ่ายฟรี','Free expense tracker')}</a><a href="./{alternate}" lang="{t('en','th')}" hreflang="{t('en','th')}">{t('English','ภาษาไทย')}</a></div></nav>
<main class="guide-shell" id="main"><nav class="crumbs" aria-label="{t('เส้นทางหน้า','Breadcrumb')}"><a href="{home}">MindSpend</a> / {title}</nav>
<header class="guide-hero"><div><span class="eyebrow">MindSpend · {t('เรื่องเงินที่เห็นภาพ','Make room for clarity')}</span><h1>{title}</h1><p class="lead">{intro}</p><p class="byline"><a href="./about.html">{t('ทีม MindSpend','MindSpend Team')}</a> · <time datetime="{DATE}">{t('10 กันยายน 2026','10 September 2026')}</time></p></div><img class="guide-mark" src="./assets/mascot/mind-think.png" alt="{t('น้องมายด์ เพื่อนคู่ใจเรื่องเงิน','Mind, your money companion')}" width="210" height="210"></header>
<article class="guide-body">{form(kind, th)}<aside class="contents" aria-label="{t('เนื้อหาในหน้านี้','On this page')}"><strong>{t('ในหน้านี้','On this page')}</strong><ul>{toc}</ul></aside>{body}</article>
<section class="related-section"><h2>{t('เรื่องที่เกี่ยวข้อง','Keep exploring')}</h2><div class="related">{cards}</div></section></main>
<footer class="guide-footer"><p>{t('MindSpend โดย Thitipong Nonnoi เป็นส่วนหนึ่งของ Jovey','MindSpend by Thitipong Nonnoi is part of Jovey')}. <a href="https://jovey.co/mindspend/">{t('เรื่องของเรา','Our story')}</a></p><a href="./privacy.html">Privacy · ไทย / English</a><a href="./support.html#contact">{t('ติดต่อทีม','Contact the team')}</a><span>© 2026 MindSpend</span></footer></body></html>
'''
    path = ROOT / filename
    if path.exists():
        existing = re.search(r'<!-- SEO:START -->.*?<!-- SEO:END -->', path.read_text(), re.S)
        if existing: source = source.replace('<!-- SEO:START --><!-- SEO:END -->', existing[0])
    return path, source

if __name__ == '__main__':
    for kind in ROUTES:
        for lang in ('th', 'en'):
            path, source = render(kind, lang)
            if '--check' in sys.argv:
                if not path.exists() or path.read_text() != source: raise SystemExit(f'{path.name}: render drift')
            else: path.write_text(source)
    print('Eight search pages verified.' if '--check' in sys.argv else 'Eight search pages rendered.')
