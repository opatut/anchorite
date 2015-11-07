export const game_state = {
    name: "Peter",
    current_tick: 1513,
    actions: [
        {
            type: "brew_action",
            recipe_id: 1,
            tick: 1523,
        },
        {
            type: "collect_action",
            tick: 1563,
        },
    ],
    inventory: [
        {
            item_type_id: 1,
            count: 12,
        },
        {
            item_type_id: 2,
            count: 7,
        },
        {
            item_type_id: 3,
            count: 2,
        },
        {
            item_type_id: 1,
            count: 12,
        },
        {
            item_type_id: 1,
            count: 12,
        },
        {
            item_type_id: 1,
            count: 12,
        },
    ],
    units: [
        {
            unit_type_id: 1,
        },
    ],
};

export const types = {
	item_types: [
		{ id: 1, name: 'Pebble', icon: 'pebble'},
		{ id: 2, name: 'Stone', icon: 'pebble'},
		{ id: 3, name: 'Rock', icon: 'pebble'},
	],
	recipes: [
		{ id: 1, unit_type_id: 1, recipe_items: [
			{ item_type_id: 1, count: 5 },
		]},
	],
	unit_types: [
		{ id: 1, name: "Pebble Heap" },
	],
};
