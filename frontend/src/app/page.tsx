"use client"; // Obligatoire dans Next.js pour utiliser des états (useState) et des formulaires

import { useState } from "react";

export default function Home() {
  // Nos variables pour stocker ce que l'utilisateur tape
  const [description, setDescription] = useState("");
  const [sizeAvg, setSizeAvg] = useState("");
  const [revenueAvg, setRevenueAvg] = useState("");
  
  // Nos variables pour l'affichage des résultats ou des erreurs
  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // La fonction qui se déclenche quand on clique sur "Prédire"
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Empêche la page de se recharger
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      // On envoie la requête à ton API FastAPI
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cleaned_description: description,
          Size_Avg: parseFloat(sizeAvg),
          Revenue_Avg_Millions: parseFloat(revenueAvg),
        }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la communication avec le modèle ML.");
      }

      const data = await response.json();
      setPrediction(data.predicted_salary_k); // On récupère la clé renvoyée par ton main.py
      
    } catch (err: any) {
      setError(err.message || "Une erreur est survenue.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      <div className="max-w-xl w-full bg-white p-8 rounded-xl shadow-lg border border-gray-100">
        <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">HR Pulse AI 🚀</h1>
        <p className="text-gray-500 mb-8 text-center text-sm">
          Prédiction de salaire basée sur les compétences et l'entreprise.
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Champ : Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description du poste (Mots-clés, compétences...)
            </label>
            <textarea
              required
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-black"
              rows={3}
              placeholder="ex: data scientist python sql machine learning..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          {/* Champ : Taille de l'entreprise */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Taille de l'entreprise (Nombre d'employés)
            </label>
            <input
              type="number"
              required
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-black"
              placeholder="ex: 5000"
              value={sizeAvg}
              onChange={(e) => setSizeAvg(e.target.value)}
            />
          </div>

          {/* Champ : Revenu de l'entreprise */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Revenu de l'entreprise (en Millions $)
            </label>
            <input
              type="number"
              required
              className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-black"
              placeholder="ex: 2000"
              value={revenueAvg}
              onChange={(e) => setRevenueAvg(e.target.value)}
            />
          </div>

          {/* Bouton de soumission */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:bg-blue-300"
          >
            {loading ? "Analyse par l'IA en cours..." : "Prédire le Salaire"}
          </button>
        </form>

        {/* Affichage des erreurs éventuelles */}
        {error && (
          <div className="mt-6 p-4 bg-red-50 text-red-700 border border-red-200 rounded-lg text-center">
            {error}
          </div>
        )}

        {/* Affichage du Résultat 🎉 */}
        {prediction !== null && (
          <div className="mt-6 p-6 bg-green-50 border border-green-200 rounded-lg text-center shadow-inner">
            <h2 className="text-sm font-semibold text-green-800 uppercase tracking-wider mb-1">
              Salaire Annuel Estimé
            </h2>
            <p className="text-4xl font-extrabold text-green-600">
              {prediction} K $
            </p>
          </div>
        )}
      </div>
    </main>
  );
}