// ==UserScript==
// @name         Accessory Shop Butterfly
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Butterfly Accessory Shop with Purple/White Theme
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var style = document.createElement('style');
    style.textContent = `
        :root {
            --purple-primary: #9b59b6;
            --purple-light: #d7bde2;
            --purple-dark: #6c3483;
            --purple-glow: rgba(155, 89, 182, 0.4);
            --white: #ffffff;
            --white-smoke: #f5f5f5;
            --shadow-purple: 0 0 30px rgba(155, 89, 182, 0.3);
        }

        .accessory-shop-header {
            background: linear-gradient(135deg, #ffffff 0%, #f0e6f6 100%);
            padding: 20px;
            border-radius: 20px;
            box-shadow: var(--shadow-purple);
            border: 2px solid var(--purple-light);
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: glowPulse 3s infinite;
        }

        .accessory-shop-header h1 {
            color: var(--purple-dark);
            font-size: 2.5em;
            font-weight: 900;
            text-shadow: 0 0 20px var(--purple-glow);
            letter-spacing: 3px;
        }

        .accessory-shop-header .butterfly-icon {
            display: inline-block;
            font-size: 3em;
            animation: fly 4s ease-in-out infinite;
            filter: drop-shadow(0 0 10px var(--purple-glow));
        }

        .accessory-card {
            background: var(--white);
            border-radius: 20px;
            padding: 20px;
            margin: 15px;
            border: 2px solid var(--purple-light);
            box-shadow: 0 5px 15px rgba(155, 89, 182, 0.15);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }

        .accessory-card::before {
            content: '🦋';
            position: absolute;
            top: -20px;
            right: -20px;
            font-size: 4em;
            opacity: 0.1;
            transform: rotate(15deg);
        }

        .accessory-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 40px rgba(155, 89, 182, 0.3);
            border-color: var(--purple-primary);
        }

        .accessory-card:hover::before {
            opacity: 0.3;
            transform: rotate(25deg) scale(1.2);
            transition: all 0.5s;
        }

        .accessory-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 15px;
            border: 3px solid var(--purple-light);
            transition: all 0.3s;
        }

        .accessory-card:hover img {
            border-color: var(--purple-primary);
            box-shadow: 0 0 30px var(--purple-glow);
        }

        .accessory-card h3 {
            color: var(--purple-dark);
            font-size: 1.3em;
            margin: 15px 0 10px;
        }

        .accessory-card .price {
            color: var(--purple-primary);
            font-size: 1.5em;
            font-weight: bold;
            text-shadow: 0 0 15px var(--purple-glow);
        }

        .accessory-card .btn-buy {
            background: linear-gradient(135deg, var(--purple-primary), var(--purple-dark));
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 15px var(--purple-glow);
            width: 100%;
            margin-top: 10px;
        }

        .accessory-card .btn-buy:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px var(--purple-glow);
            background: linear-gradient(135deg, var(--purple-dark), var(--purple-primary));
        }

        .butterfly-float {
            position: fixed;
            pointer-events: none;
            font-size: 2em;
            animation: floatButterfly 8s ease-in-out infinite;
            opacity: 0.6;
            z-index: 9999;
        }

        @keyframes floatButterfly {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg) scale(1);
            }
            25% {
                transform: translate(50px, -100px) rotate(10deg) scale(1.1);
            }
            50% {
                transform: translate(100px, 0) rotate(-5deg) scale(0.9);
            }
            75% {
                transform: translate(50px, 100px) rotate(15deg) scale(1.1);
            }
        }

        @keyframes fly {
            0%, 100% {
                transform: translateY(0) rotate(-5deg);
            }
            50% {
                transform: translateY(-20px) rotate(5deg);
            }
        }

        @keyframes glowPulse {
            0%, 100% {
                box-shadow: var(--shadow-purple);
            }
            50% {
                box-shadow: 0 0 60px rgba(155, 89, 182, 0.5);
            }
        }

        .dynamic-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 20% 50%, rgba(155, 89, 182, 0.05) 0%, transparent 50%),
                        radial-gradient(circle at 80% 50%, rgba(155, 89, 182, 0.05) 0%, transparent 50%),
                        #ffffff;
            z-index: -1;
        }

        .shop-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            padding: 20px 0;
        }
    `;
    document.head.appendChild(style);

    var bg = document.createElement('div');
    bg.className = 'dynamic-bg';
    document.body.prepend(bg);

    function createButterflies() {
        var butterflies = ['🦋', '🦋', '🦋', '🦋', '🦋'];
        for (var i = 0; i < butterflies.length; i++) {
            var el = document.createElement('div');
            el.className = 'butterfly-float';
            el.textContent = butterflies[i];
            el.style.left = Math.random() * 100 + '%';
            el.style.top = Math.random() * 100 + '%';
            el.style.animationDelay = (i * 1.5) + 's';
            el.style.animationDuration = (6 + Math.random() * 4) + 's';
            el.style.fontSize = (1.5 + Math.random() * 2) + 'em';
            document.body.appendChild(el);
        }
    }
    createButterflies();

    function createShop() {
        var container = document.createElement('div');
        container.className = 'shop-container';

        var header = document.createElement('div');
        header.className = 'accessory-shop-header';
        header.innerHTML = `
            <div class="butterfly-icon">🦋</div>
            <h1>✨ Butterfly Accessory ✨</h1>
            <p style="color: var(--purple-primary); font-size: 1.2em;">
                Experience beauty with butterflies
            </p>
        `;
        container.appendChild(header);

        var products = [
            { name: 'Butterfly Necklace', price: '250,000 T', img: 'https://via.placeholder.com/300x200/9b59b6/ffffff?text=🦋' },
            { name: 'Butterfly Bracelet', price: '180,000 T', img: 'https://via.placeholder.com/300x200/d7bde2/6c3483?text=🦋' },
            { name: 'Butterfly Earrings', price: '320,000 T', img: 'https://via.placeholder.com/300x200/6c3483/ffffff?text=🦋' },
            { name: 'Butterfly Pin', price: '150,000 T', img: 'https://via.placeholder.com/300x200/f0e6f6/9b59b6?text=🦋' },
            { name: 'Butterfly Hat', price: '450,000 T', img: 'https://via.placeholder.com/300x200/9b59b6/d7bde2?text=🦋' },
            { name: 'Butterfly Bag', price: '580,000 T', img: 'https://via.placeholder.com/300x200/d7bde2/ffffff?text=🦋' }
        ];

        var grid = document.createElement('div');
        grid.className = 'products-grid';

        for (var i = 0; i < products.length; i++) {
            var p = products[i];
            var card = document.createElement('div');
            card.className = 'accessory-card';
            card.innerHTML = `
                <img src="${p.img}" alt="${p.name}" loading="lazy">
                <h3>${p.name}</h3>
                <div class="price">${p.price}</div>
                <button class="btn-buy" onclick="alert('🦋 ${p.name} added to cart!')">
                    🛒 Buy Now
                </button>
            `;
            grid.appendChild(card);
        }

        container.appendChild(grid);
        document.body.prepend(container);

        document.addEventListener('click', function(e) {
            var butterfly = document.createElement('div');
            butterfly.textContent = '🦋';
            butterfly.style.position = 'fixed';
            butterfly.style.left = e.pageX + 'px';
            butterfly.style.top = e.pageY + 'px';
            butterfly.style.fontSize = '3em';
            butterfly.style.pointerEvents = 'none';
            butterfly.style.transition = 'all 1s ease-out';
            butterfly.style.opacity = '1';
            document.body.appendChild(butterfly);

            setTimeout(function() {
                butterfly.style.transform = 'translateY(-200px) scale(2) rotate(180deg)';
                butterfly.style.opacity = '0';
            }, 50);

            setTimeout(function() {
                butterfly.remove();
            }, 1050);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createShop);
    } else {
        createShop();
    }

})();