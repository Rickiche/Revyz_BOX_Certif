        function jouer(retrait) {
            const form = document.createElement('form');
            form.method = 'POST';
            const actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.value = 'jouer';
            const retraitInput = document.createElement('input');
            retraitInput.type = 'hidden';
            retraitInput.name = 'retrait';
            retraitInput.value = retrait;
            form.appendChild(actionInput);
            form.appendChild(retraitInput);
            document.body.appendChild(form);
            form.submit();
        }
        
        function nouvellePartie() {
            const form = document.createElement('form');
            form.method = 'POST';
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'action';
            input.value = 'reinitialiser';
            form.appendChild(input);
            document.body.appendChild(form);
            form.submit();
        }
        
        function afficherRegles() {
            window.open('?action=regles', 'Règles', 'width=550,height=650,scrollbars=yes');
        }