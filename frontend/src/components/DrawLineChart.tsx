import { useState, useRef, useEffect, MouseEvent, TouchEvent } from 'react';
import ReactEcharts from 'echarts-for-react';
import axios from 'axios';
import {
    ToggleButton, ToggleButtonGroup, Grid, Button, Dialog, DialogTitle,
    DialogContent, TextField, DialogActions
} from '@mui/material';

type UUID = string;

interface DrawLineChartParams {
    session_id: UUID,
    onPointSelect: (x: number, y: number) => void;
}

interface DataPoint {
    x: number;
    y: number;
}

interface PointDetails {
    whatHappened: string;
    whenHappened: string;
    thoughts: string;
    feelings: string;
    actionsTaken: string;
    consequences: string;
}

interface SelectedPoint extends DataPoint {
    details: PointDetails;
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
    const [selectedPoints, setSelectedPoints] = useState<SelectedPoint[]>([]);
    const [open, setOpen] = useState(false);
    const [currentPoint, setCurrentPoint] = useState<SelectedPoint | null>(null);
    const [confirmDialogOpen, setConfirmDialogOpen] = useState(false); // Confirmation dialog state
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
            selectOrEditDataPoint(e);
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

    const selectOrEditDataPoint = (e: MouseEvent | Touch) => {
        const chart = chartRef.current?.getEchartsInstance();
        if (!chart) return;

        const chartRect = chart.getDom().getBoundingClientRect();
        const pointInPixel = [e.clientX - chartRect.left, e.clientY - chartRect.top];
        const pointInGrid = chart.convertFromPixel({ seriesIndex: 0 }, pointInPixel);

        if (!pointInGrid) return;

        const x = pointInGrid[0];

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

        const existingPoint = selectedPoints.find(point => point.x === selectedPoint.x && point.y === selectedPoint.y);

        if (existingPoint) {
            setCurrentPoint(existingPoint);
        } else {
            setCurrentPoint({
                ...selectedPoint,
                details: {
                    whatHappened: '',
                    whenHappened: '',
                    thoughts: '',
                    feelings: '',
                    actionsTaken: '',
                    consequences: '',
                },
            });
        }

        setOpen(true);
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

                return { ...point, x: data[closestIndex].x, y: data[closestIndex].y };
            });
        });
    };

    const handleClose = () => {
        setOpen(false);
        setCurrentPoint(null);
    };

    const handleSubmitPoint = () => {
        if (currentPoint) {
            setSelectedPoints((prevPoints) => {
                const pointIndex = prevPoints.findIndex(
                    (point) => point.x === currentPoint.x && point.y === currentPoint.y
                );

                if (pointIndex > -1) {
                    const updatedPoints = [...prevPoints];
                    updatedPoints[pointIndex] = currentPoint;
                    return updatedPoints;
                } else {
                    return [...prevPoints, currentPoint];
                }
            });
        }
        handleClose();
        params.onPointSelect(currentPoint!.x, currentPoint!.y);
    };

    const handleSubmitAll = async () => {
        setConfirmDialogOpen(false);

        try {
            // Submit the curve data using axios
            const curveResponse = await axios.post('/api/curves', {
                session: params.session_id,
                data: data.map((datapoint) => datapoint.y),
            });

            const curveResult = curveResponse.data;

            // Submit keypoints after curve has been created
            const keypointPromises = selectedPoints.map(point =>
                axios.post('/api/keymoments', {
                    xvalue: point.x,
                    yvalue: point.y,
                    what: point.details.whatHappened,
                    when: point.details.whenHappened,
                    thoughts: point.details.thoughts,
                    feelings: point.details.feelings,
                    actions: point.details.actionsTaken,
                    consequences: point.details.consequences,
                    session: curveResult.session,  // Ensure correct session ID
                    curve: curveResult.id,         // Associate with curve ID
                })
            );

            const keypointResults = await Promise.all(keypointPromises);

            if (keypointResults.some(response => response.status !== 200)) {
                throw new Error('Failed to submit one or more key points');
            }

            alert('Data submitted successfully!');
        } catch (error) {
            console.error('Submission error:', error);
            alert('Failed to submit data');
        }
    };

    const isFormValid = () => {
        return currentPoint && Object.values(currentPoint.details).every((value) => value.trim() !== '');
    };

    const getOption = () => {
        return {
            xAxis: {
                type: 'value',
                min: 0,
                max: 100,
                interval: 12.5,
                axisLabel: {
                    show: true,
                    formatter: (value: number) => {
                        if (value === 12.5) return 'Before';
                        if (value === 50) return 'During';
                        if (value === 87.5) return 'After';
                        return '';
                    },
                    fontSize: 12,
                    fontWeight: 'bold',
                    margin: 15,
                },
                splitLine: {
                    show: true,
                },
                axisLine: {
                    lineStyle: {
                        color: 'black',
                    },
                },
                axisTick: {
                    show: true,
                    alignWithLabel: true,
                },
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 100,
                name: 'Learning Intensity',
                interval: 25,
                axisLabel: {
                    show: true,
                    formatter: (value: number) => {
                        if (value === 25) return 'Low';
                        if (value === 50) return 'Medium';
                        if (value === 75) return 'High';
                        return '';
                    },
                    fontSize: 12,
                    fontWeight: 'bold',
                    margin: 15,
                },
                axisLine: {
                    lineStyle: {
                        color: 'black',
                    },
                },
                splitLine: {
                    show: true,
                },
                axisTick: {
                    show: true,
                    alignWithLabel: true,
                },
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
                    z: 10,
                    label: {
                        show: true,
                        formatter: (params: any) => {
                            const point = selectedPoints.find(p => p.x === params.data[0] && p.y === params.data[1]);
                            if (!point) return '';

                            const maxLength = 20;
                            const { whatHappened } = point.details;
                            if (whatHappened.length > maxLength) {
                                return whatHappened.substring(0, maxLength) + '...';
                            }
                            return whatHappened;
                        },
                        position: 'top',
                        color: 'black',
                        fontSize: 12,
                        fontWeight: 'bold',
                    },
                    emphasis: {
                        label: {
                            show: true,
                            color: 'black',
                        },
                    },
                },
                {
                    type: 'line',
                    markLine: {
                        silent: true,
                        symbol: ['none', 'none'],
                        label: { show: false },
                        lineStyle: {
                            color: 'rgba(0, 0, 0, 0.5)',
                            type: 'solid',
                            width: 2,
                        },
                        data: [
                            { xAxis: 25 },
                            { xAxis: 75 },
                        ],
                        z: 1,
                    },
                },
            ],
        };
    };

    return (
        <>
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
                <Grid item xs={12} style={{
                    height: 56,
                    paddingLeft: '10%',
                    paddingRight: '10%',
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between'
                }}>
                    <ToggleButtonGroup
                        value={mode}
                        exclusive
                        onChange={(_, newMode) => setMode(newMode)}
                        style={{ display: 'flex', justifyContent: 'center', width: '75%' }}
                    >
                        <ToggleButton value="draw" style={{ flexGrow: 1, minWidth: 100 }}>Draw</ToggleButton>
                        <ToggleButton value="select" style={{ flexGrow: 1, minWidth: 100 }}>Select</ToggleButton>
                    </ToggleButtonGroup>
                    <Button onClick={() => setConfirmDialogOpen(true)}>Submit</Button>
                </Grid>
            </Grid>

            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Details for Selected Point</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="What Happened"
                        fullWidth
                        value={currentPoint?.details.whatHappened}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, whatHappened: e.target.value } } : prev)
                        }
                        required
                    />
                    <TextField
                        margin="dense"
                        label="When Did It Happen"
                        fullWidth
                        value={currentPoint?.details.whenHappened}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, whenHappened: e.target.value } } : prev)
                        }
                        required
                    />
                    <TextField
                        margin="dense"
                        label="Thoughts"
                        fullWidth
                        value={currentPoint?.details.thoughts}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, thoughts: e.target.value } } : prev)
                        }
                        required
                    />
                    <TextField
                        margin="dense"
                        label="Feelings"
                        fullWidth
                        value={currentPoint?.details.feelings}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, feelings: e.target.value } } : prev)
                        }
                        required
                    />
                    <TextField
                        margin="dense"
                        label="Actions Taken"
                        fullWidth
                        value={currentPoint?.details.actionsTaken}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, actionsTaken: e.target.value } } : prev)
                        }
                        required
                    />
                    <TextField
                        margin="dense"
                        label="Consequences"
                        fullWidth
                        value={currentPoint?.details.consequences}
                        onChange={(e) =>
                            setCurrentPoint((prev) => prev ? { ...prev, details: { ...prev.details, consequences: e.target.value } } : prev)
                        }
                        required
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button onClick={handleSubmitPoint} disabled={!isFormValid()}>Submit</Button>
                </DialogActions>
            </Dialog>

            <Dialog open={confirmDialogOpen} onClose={() => setConfirmDialogOpen(false)}>
                <DialogTitle>Confirm Submission</DialogTitle>
                <DialogContent>
                    Are you sure you want to submit your data? This action cannot be undone.
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setConfirmDialogOpen(false)}>Cancel</Button>
                    <Button onClick={handleSubmitAll}>Submit</Button>
                </DialogActions>
            </Dialog>
        </>
    );
};
