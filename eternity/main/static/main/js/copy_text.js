function copyFunc() {
    // ищем нужный элемент по его id
    let cpTxt = document.getElementById('copyText')
    // выделяем текст
    let range = document.createRange()
    range.selectNode(cpTxt)
    window.getSelection().addRange(range)

    // пытаемся скопировать текст в буфер обмена
    try {
        document.execCommand('copy')
        console.log('Текст успешно скопирован ' + cpTxt)
        // alert("Текст скопирован в буфер обмена!")
    } catch(err) {
        console.log("Не могу скопировать текст")
    }
    // снимаем выделение текста
    // window.getSelection().removeAllRanges()
}
