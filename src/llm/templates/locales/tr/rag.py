from string import Template

system_prompt = Template("\n".join([
    "Kullanıcıya yanıt üretmek için bir asistansın.",
    "Kullanıcının sorgusuyla ilişkili bir dizi doküman verilecektir.",
    "Yanıtını yalnızca verilen dokümanlara dayanarak oluşturmalısın.",
    "Kullanıcının sorusuyla ilgisiz dokümanları dikkate alma.",
    "Eğer uygun bir yanıt oluşturamıyorsan kullanıcıdan özür dileyebilirsin.",
    "Yanıtı, kullanıcının sorusuyla aynı dilde üretmelisin.",
    "Kibar ve saygılı bir dil kullan.",
    "Yanıtın kısa, net ve gereksiz detaylardan arındırılmış olsun.",
]))


document_prompt = Template("\n".join([
    "## Doküman No: $doc_num",
    "### İçerik: $chunk_text"
]))


footer_prompt = Template("\n".join([
    "Yalnızca yukarıdaki dokümanlara dayanarak aşağıdaki soruyu yanıtla.",
    "## Soru: $question",
    "### Cevap:"
]))