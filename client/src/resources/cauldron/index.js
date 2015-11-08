import baseSprite from './base.png';
import brewSprite from './brew.png';

export const base = {
	width: 32,
	height: 32,
	sprite: baseSprite,
	count: 4,
	frames: [0, 1, 2, 3],
	framerate: 4,
};

export const brew = {
	width: 32,
	height: 32,
	sprite: brewSprite,
	count: 4,
	frames: [0, 1, 2, 3],
	framerate: 8,
};
