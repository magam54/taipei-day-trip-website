// 動態卡片製作處理
function makebox(data){
    let len=data.data.length
    for (n=0 ; n < len ; n++){
        let title = data.data[n].name;
        let mrt = data.data[n].mrt;
        let cat = data.data[n].category;
        let id =data.data[n].id;
        let images = data.data[n].images[0];
        let gridLi = document.getElementById('gridLi');
        let card = document.createElement('div');
            card.classList.add('card');
        let img = document.createElement('img');
            img.src = images;
        let p1 = document.createElement('p');
            p1.classList.add('a');
            p1.textContent=title
        let p2 = document.createElement('p');
            p2.classList.add('b');
            p2.textContent=mrt;
        let span = document.createElement('span');
            span.classList.add('c');
            span.textContent=cat;
        let link = document.createElement('a');
        link.setAttribute('href','http://18.139.199.228:3000//attraction/'+id)
            card.append(img,p1,p2,span);
            link.append(card);
            gridLi.append(link);
    }
}

// 設定初始頁面網址&偵測對象
let url = new URL('http://18.139.199.228:3000/api/attractions?page=0')
let footer = document.getElementById("footer")

// 初始頁面且偵測滾動
function callback(entries){
    if(entries[0].isIntersecting){
        fetch(url)
        .then(function(taipei){
            return taipei.json();
        })
        .then(function(data){
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
            }
            if(p==null){
                makebox(data);
                oberserver.unobserve(footer)
            }
        })
    }
}

const oberserver = new IntersectionObserver (callback)
oberserver.observe(footer);

// 關鍵字搜索偵測滾動
function callbackKeyword(entries){
    if(entries[0].isIntersecting){
        let keyword = document.getElementById("kw").value;
        url.searchParams.set("keyword",keyword);
        fetch(url)
        .then(function(taipei){
            return taipei.json();
        })
        .then(function(data){
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
            }
            if(p==null){
                makebox(data);
                oberserverKW.unobserve(footer)
            }
        })
    }
}

const oberserverKW = new IntersectionObserver (callbackKeyword)

// 關鍵字搜索 點擊放大鏡觸發
document.getElementById("manifier").addEventListener("click",function(){
    keywordSearch()
})

// 關鍵字 按Enter觸發
document.getElementById("kw").addEventListener("keyup",function(e){
    if(e.key==="Enter"){
        keywordSearch()
    }
})

// 關鍵字搜尋
function keywordSearch(){
    oberserver.unobserve(footer)
    let keyword = document.getElementById("kw").value;
    url.searchParams.set("page",0);
    url.searchParams.set("keyword",keyword);
    let gridLi = document.getElementById("gridLi")
    fetch(url)
    .then(function(taipei){
        return taipei.json();
    })
    .then(function(data){
        let len=data.data.length
        if(len != 0){
            gridLi.innerHTML=""
            let p = data.nextPage
            if(p!=null){
                makebox(data);
                url.searchParams.set("page",p);
                oberserverKW.observe(footer);
            }
            if(p==null){
                makebox(data);
            }
        }
        if(len == 0){
            gridLi.innerHTML=""
            let ms = document.createElement('p');
            ms.textContent='找不到相關景點資料！'
            gridLi.append(ms);
        }   
    })
}