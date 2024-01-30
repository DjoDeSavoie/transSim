-- SCRIPT POUR LA MODIFICATION / AJOUT DE VALEURS et PROPRIETES / SUPPRESSION DE VALEURS et PROPRIETE



-- Delete all the values from cartebancaire
-- DELETE FROM comptebancaireemetteur; 


INSERT INTO comptebancaireacquereur (
    idCompteAcquereur,
    idBanqueAcquereur,
    nom,
    prenom,
    soldeCompteAcquereur
  )
VALUES (
    '1',
    1,
    'Decathlon',
    'Les Terrasses du Port',
    100000
  );
