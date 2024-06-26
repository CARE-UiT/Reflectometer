import React, { useState, useRef, useEffect, MouseEvent } from 'react';
import ReactEcharts from 'echarts-for-react';
import * as echarts from 'echarts';
import { Button, ButtonGroup } from '@mui/material';

interface DataPoint {
    x: number;
    y: number;
}

const POINTS_COUNT = 100;
const WIDTH = 500;  // Width of the chart
const HEIGHT = 500;  // Height of the chart

const initializeData = () => {
    const data: DataPoint[] = [];
    const step = WIDTH / (POINTS_COUNT - 1);
    for (let i = 0; i < POINTS_COUNT; i++) {
        data.push({ x: i * step, y: 0 });
    }
    return data;
};

const DrawLineChart: React.FC = () => {
    const [data, setData] = useState<DataPoint[]>(initializeData());
    const [isDrawing, setIsDrawing] = useState<boolean>(false);
    const [mode, setMode] = useState<'draw' | 'select'>('draw');
    const chartRef = useRef<ReactEcharts>(null);

    useEffect(() => {
        const handleResize = () => {
            if (chartRef.current) {
                chartRef.current.getEchartsInstance().resize();
            }
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const handleMouseDown = () => {
        if (mode === 'draw') {
            setIsDrawing(true);
        }
    };

    const handleMouseUp = () => {
        if (mode === 'draw') {
            setIsDrawing(false);
        }
    };

    const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
        if (mode === 'draw' && isDrawing) {
            updateDataPoint(e);
        }
    };

    const handleClick = (e: MouseEvent<HTMLDivElement>) => {
        if (mode === 'select') {
            selectDataPoint(e);
        }
    };

    const updateDataPoint = (e: MouseEvent<HTMLDivElement>) => {
        const chart = chartRef.current?.getEchartsInstance();
        if (!chart) return;

        const pointInPixel = [e.clientX, e.clientY];
        const pointInGrid = chart.convertFromPixel({ seriesIndex: 0 }, pointInPixel);

        const x = pointInGrid[0];
        const y = pointInGrid[1];

        setData((prevData) => {
            const newData = [...prevData];
            let closestIndex = 0;
            let closestDistance = Math.abs(newData[0].x - x);

            for (let i = 1; i < newData.length; i++) {
                const distance = Math.abs(newData[i].x - x);
                if (distance < closestDistance) {
                    closestDistance = distance;
                    closestIndex = i;
                }
            }

            newData[closestIndex].y = y;
            return newData;
        });
    };

    const selectDataPoint = (e: MouseEvent<HTMLDivElement>) => {
        const chart = chartRef.current?.getEchartsInstance();
        if (!chart) return;

        const pointInPixel = [e.clientX, e.clientY];
        const pointInGrid = chart.convertFromPixel({ seriesIndex: 0 }, pointInPixel);

        const x = pointInGrid[0];
        const y = pointInGrid[1];

        console.log(`Selected point: (${x}, ${y})`);
        // Additional logic for selected key points can be added here
    };

    const getOption = () => {
        return {
            xAxis: {
                type: 'value',
                min: 0,
                max: WIDTH,  // Adjust based on your requirements
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: HEIGHT,  // Adjust based on your requirements
            },
            series: [
                {
                    type: 'line',
                    data: data.map((point) => [point.x, point.y]),
                    smooth: true,
                    lineStyle: {
                        width: 2,
                    },
                },
            ],
        };
    };

    return (
        <div>
            <ButtonGroup variant="contained" aria-label="outlined primary button group">
                <Button onClick={() => setMode('draw')} color={mode === 'draw' ? 'primary' : 'inherit'}>Draw</Button>
                <Button onClick={() => setMode('select')} color={mode === 'select' ? 'primary' : 'inherit'}>Select</Button>
            </ButtonGroup>
            <div
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}
                onMouseMove={handleMouseMove}
                onClick={handleClick}
                style={{ width: `${WIDTH}px`, height: `${HEIGHT}px`, border: '1px solid #ccc' }}
            >
                <ReactEcharts
                    ref={chartRef}
                    option={getOption()}
                    style={{ width: '100%', height: '100%' }}
                />
            </div>
        </div>
    );
};

export default DrawLineChart;
