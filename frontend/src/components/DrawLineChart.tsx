import React, { useState, useRef, useEffect, MouseEvent, TouchEvent } from 'react';
import ReactEcharts from 'echarts-for-react';
import { ToggleButton, ToggleButtonGroup, Grid } from '@mui/material';

interface DrawLineChartParams {
    onPointSelect: (x: number, y: number) => void;
}

interface DataPoint {
    x: number;
    y: number;
}

const POINTS_COUNT = 150;

const initializeData = () => {
    const data: DataPoint[] = [];
    const step = 100 / (POINTS_COUNT - 1);
    for (let i = 0; i < POINTS_COUNT; i++) {
        data.push({ x: i * step, y: 0 });
    }
    return data;
};

export const DrawLineChart = (params: DrawLineChartParams) => {
    const [data, setData] = useState<DataPoint[]>(initializeData());
    const [isDrawing, setIsDrawing] = useState<boolean>(false);
    const [mode, setMode] = useState<'draw' | 'select'>('draw');
    const [selectedPoints, setSelectedPoints] = useState<DataPoint[]>([]);
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
            updateSelectedPoints();
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

    const handleTouchStart = () => {
        if (mode === 'draw') {
            setIsDrawing(true);
        }
    };

    const handleTouchEnd = () => {
        if (mode === 'draw') {
            setIsDrawing(false);
            updateSelectedPoints();
        }
    };

    const handleTouchMove = (e: TouchEvent<HTMLDivElement>) => {
        if (mode === 'draw' && isDrawing) {
            const touch = e.touches[0];
            updateDataPoint(touch);
        }
    };

    const handleTouchClick = (e: TouchEvent<HTMLDivElement>) => {
        if (mode === 'select') {
            const touch = e.changedTouches[0];
            selectDataPoint(touch);
        }
    };

    const updateDataPoint = (e: MouseEvent | Touch) => {
        const chart = chartRef.current?.getEchartsInstance();
        if (!chart) return;

        const chartRect = chart.getDom().getBoundingClientRect();
        const pointInPixel = [e.clientX - chartRect.left, e.clientY - chartRect.top];
        const pointInGrid = chart.convertFromPixel({ seriesIndex: 0 }, pointInPixel);

        if (!pointInGrid) return;

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

    const selectDataPoint = (e: MouseEvent | Touch) => {
        const chart = chartRef.current?.getEchartsInstance();
        if (!chart) return;

        const chartRect = chart.getDom().getBoundingClientRect();
        const pointInPixel = [e.clientX - chartRect.left, e.clientY - chartRect.top];
        const pointInGrid = chart.convertFromPixel({ seriesIndex: 0 }, pointInPixel);

        if (!pointInGrid) return;

        const x = pointInGrid[0];

        // Find the closest point in the x-axis
        let closestIndex = 0;
        let closestDistance = Math.abs(data[0].x - x);

        for (let i = 1; i < data.length; i++) {
            const distance = Math.abs(data[i].x - x);
            if (distance < closestDistance) {
                closestDistance = distance;
                closestIndex = i;
            }
        }

        const selectedPoint = { x: data[closestIndex].x, y: data[closestIndex].y };
        setSelectedPoints((prevPoints) => {
            const newPoints = [...prevPoints];
            if (!newPoints.some(point => point.x === selectedPoint.x && point.y === selectedPoint.y)) {
                newPoints.push(selectedPoint);
            }
            return newPoints;
        });

        params.onPointSelect(selectedPoint.x, selectedPoint.y);
    };

    const updateSelectedPoints = () => {
        setSelectedPoints((prevPoints) => {
            return prevPoints.map((point) => {
                let closestIndex = 0;
                let closestDistance = Math.abs(data[0].x - point.x);

                for (let i = 1; i < data.length; i++) {
                    const distance = Math.abs(data[i].x - point.x);
                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestIndex = i;
                    }
                }

                return { x: data[closestIndex].x, y: data[closestIndex].y };
            });
        });
    };

    const getOption = () => {
        return {
            xAxis: {
                type: 'value',
                min: 0,
                max: 100,
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 100,
            },
            series: [
                {
                    type: 'line',
                    data: data.map((point) => [point.x, point.y]),
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        width: 2,
                    },
                },
                {
                    type: 'scatter',
                    data: selectedPoints.map((point) => [point.x, point.y]),
                    symbolSize: 10,
                    itemStyle: {
                        color: 'red',
                    },
                    z: 10,  // This ensures the selected points appear above the line
                },
            ],
        };
    };

    return (
        <Grid container spacing={2} style={{ height: '100%' }}>
            <Grid item xs={12} style={{ height: 'calc(100% - 56px)' }}>
                <div
                    onMouseDown={handleMouseDown}
                    onMouseUp={handleMouseUp}
                    onMouseMove={handleMouseMove}
                    onClick={handleClick}
                    onTouchStart={handleTouchStart}
                    onTouchEnd={handleTouchEnd}
                    onTouchMove={handleTouchMove}
                    style={{ width: '100%', height: '100%', border: 'none' }}
                >
                    <ReactEcharts
                        ref={chartRef}
                        option={getOption()}
                        style={{ width: '100%', height: '100%' }}
                    />
                </div>
            </Grid>
            <Grid item xs={12} style={{ height: 56 }}>
                <ToggleButtonGroup
                    value={mode}
                    exclusive
                    onChange={(_, newMode) => setMode(newMode)}
                    style={{ display: 'flex', justifyContent: 'center', width: '100%' }}
                >
                    <ToggleButton value="draw" style={{ flexGrow: 1, minWidth: 100 }}>Draw</ToggleButton>
                    <ToggleButton value="select" style={{ flexGrow: 1, minWidth: 100 }}>Select</ToggleButton>
                </ToggleButtonGroup>
            </Grid>
        </Grid>
    );
};
