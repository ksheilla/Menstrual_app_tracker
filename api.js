require('dotenv').config();
const express = require('express');
const fetch = require('node-fetch');
const router = express.Router();

// Tasty API Key and Host
const RAPID_API_KEY =process.env.RAPID_API_KEY;
const RAPID_API_HOST = 'tasty.p.rapidapi.com';

// Nutritional Tags for Each Menstrual Phase
const PHASE_TAGS = {
    'menstruation': 'iron-rich foods',
    'follicular': 'hormone-balancing foods',
    'ovulation': 'high-protein foods',
    'luteal': 'mood-supporting foods'
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
        const query = PHASE_TAGS[phase];

        const response = await fetch(
            `https://tasty.p.rapidapi.com/recipes/list`,
            {
                method: 'GET',
                headers: {
                    'X-RapidAPI-Key': RAPID_API_KEY,
                    'X-RapidAPI-Host': RAPID_API_HOST
                },
                params: {
                    q: query,
                    tags: 'under_30_minutes', // Optional: Filter for quick recipes
                    size: 5 // Limit the number of results
                }
            }
        );

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();

        // Enrich Recipes with Nutritional Information
        const enrichedRecipes = data.results.map(recipe => ({
            id: recipe.id,
            title: recipe.name,
            image: recipe.thumbnail_url,
            phaseBenefits: PHASE_BENEFITS[phase],
            description: recipe.description || 'No description available',
            instructions: recipe.instructions ? recipe.instructions.map(step => step.display_text) : ['No instructions available']
        }));

        res.json(enrichedRecipes);
    } catch (error) {
        console.error('Error fetching recipes:', error);
        res.status(500).json({ error: 'Failed to fetch recipes' });
    }
});

module.exports = router;