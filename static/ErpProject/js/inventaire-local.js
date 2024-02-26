inventaireLocal = {};
/*
    Une ligne de la inventaire est un objet JSON de type :
    {
        ligne_id,
        article_id,
        nom_article,
        stock_article_id,
        quantite_demandee,
        quantite_fournie,
        unite_achat_id,
        prix_unitaire,
        prix_lot,
        symbole_unite,
        type
    }
*/
inventaireLocal.ajouterLigneInventaire = function (ligne) {
    ligne.type = "ligne-inventaire";
    var data = JSON.stringify(ligne);
    localStorage.setItem(ligne.ligne_id, data);
};

/*
    Un ordre de inventaire est un objet JSON de type :
    {
        numero,
        date_prevue,
        date_realisation,
        est_realisee,
        devise_id,
        condition_reglement_id,
        fournisseur_id,
        receveur_id,
        reference_document,
        description
    }
*/
inventaireLocal.ajouterInventaire = function (ordre) {
    var data = JSON.stringify(ordre);
    localStorage.setItem("inventaire", data);
};

// Modifier la quantité d'une ligne de inventaire
inventaireLocal.modifierQuantite = function (ligne_id, quantite_demandee, quantite_fournie) {
    var data = localStorage.getItem(ligne_id);
    if(data != null && data != "" && ligne_id != "lsid")
    {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-inventaire")
        {
            ligne.quantite_demandee = quantite_demandee;
            ligne.quantite_fournie = quantite_fournie;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

inventaireLocal.modifierPrix = function (ligne_id, prix_unitaire, prix_lot) {
    var data = localStorage.getItem(ligne_id);
    if (data != null && data != "" && ligne_id != "lsid") {
        var ligne = JSON.parse(data);
        if (ligne.type == "ligne-inventaire")
        {
            ligne.prix_unitaire = prix_unitaire;
            ligne.prix_lot = prix_lot;
            data = JSON.stringify(ligne);
            localStorage.setItem(ligne_id, data);
        }
    }
};

inventaireLocal.supprimerLigne = function (ligne_id) {
    if(ligne_id != null && ligne_id != "" && ligne_id != "lsid") localStorage.removeItem(ligne_id);
};

inventaireLocal.supprimerInventaire = function () {
    this.supprimerToutesLignes();
    localStorage.removeItem("inventaire");
};

inventaireLocal.supprimerToutesLignes = function () {
    var lignesInventaire = new Array();
    for (var i = 0; i < localStorage.length; i++)
    {
        var ligne_id = localStorage.key(i);
        if (ligne_id != "lsid" && ligne_id != "inventaire" 
            && ligne_id != "commande" && ligne_id != "inventaire"
            && ligne_id != "transformation" && ligne_id != "fabrication"
        )
        {
            var data = localStorage.getItem(ligne_id);
            var ligne = JSON.parse(data);
            if (ligne.type == "ligne-inventaire") lignesInventaire.push(ligne);
        }
    }
    for(var i = 0; i < lignesInventaire.length; i++)
    {
        var ligne = lignesInventaire[i];
        localStorage.removeItem(ligne.ligne_id);
    }
};

inventaireLocal.avoirToutesLignes = function () {
    var nombreItems = localStorage.length;
    var listeLignes = new Array();
    for(var i = 0; i < nombreItems; i++)
    {
        var ligne_id = localStorage.key(i);
        if (ligne_id != "lsid" && ligne_id != "inventaire" 
            && ligne_id != "commande" && ligne_id != "inventaire"
            && ligne_id != "transformation" && ligne_id != "fabrication"
        )
        {
            var data = localStorage.getItem(ligne_id);
            var ligne = JSON.parse(data);
            listeLignes.push(ligne);
        }
    }
    return listeLignes;
};

inventaireLocal.avoirInventaire = function () {
    var inventaire = null;
    var data = localStorage.getItem("inventaire");
    if (data != null && data != "") inventaire = JSON.parse(data);
    return inventaire;
};

inventaireLocal.refresh = function()
{
    localStorage.clear();
}