const express = require('express');
const fetch = require('node-fetch');
const router = express.Router();

const RAPID_API_KEY = '34bf7c9b10msh8b32e483c57424cp120256jsn52ce1154613c';
const RAPID_API_HOST = 'spoonacular-recipe-food-nutrition-v1.p.rapidapi.com';

// Nutritional Tags for Each Menstrual Phase
const PHASE_TAGS = {
    'menstruation': ['iron-rich', 'anti-inflammatory'],
    'follicular': ['energy-boosting', 'hormone-balancing'],
    'ovulation': ['omega-3', 'hormone-balancing'],
    'luteal': ['magnesium-rich', 'mood-supporting']
};

// Health Benefits for Each Phase
const PHASE_BENEFITS = {
    'menstruation': 'Supports iron replenishment and reduces inflammation during menstrual flow',
    'follicular': 'Provides energy and supports hormonal balance as your body prepares for ovulation',
    'ovulation': 'Helps maintain hormonal balance and supports overall reproductive health',
    'luteal': 'Assists in mood regulation and provides nutritional support before menstruation'
};

// API Route: Get Food Recommendations Based on Menstrual Phase
router.get('/recommendations/:phase', async (req, res) => {
    const phase = req.params.phase.toLowerCase();

    // Validate Phase
    if (!PHASE_TAGS[phase]) {
        return res.status(400).json({ error: 'Invalid menstrual phase' });
    }

    try {
        const tag = PHASE_TAGS[phase][Math.floor(Math.random() * PHASE_TAGS[phase].length)];
        
        const response = await fetch(
            `https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random?tags=${tag}&number=3`, 
            {
                method: 'GET',
                headers: {
                    'x-rapidapi-key': RAPID_API_KEY,
                    'x-rapidapi-host': RAPID_API_HOST
                }
            }
        );

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();
        
        // Enrich Recipes with Nutritional Information
        const enrichedRecipes = data.recipes.map(recipe => ({
            id: recipe.id,
            title: recipe.title,
            image: recipe.image,
            phaseBenefits: PHASE_BENEFITS[phase],
            nutritionalTag: tag,
            instructions: recipe.instructions || 'No instructions available'
        }));

        res.json(enrichedRecipes);
    } catch (error) {
        console.error('Error fetching recipes:', error);
        res.status(500).json({ error: 'Failed to fetch recipes' });
    }
});

module.exports = router;
