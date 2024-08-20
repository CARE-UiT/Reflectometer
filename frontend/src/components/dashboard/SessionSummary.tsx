import * as React from 'react';
import { useEffect, useState, useMemo } from 'react';
import ReactEcharts from 'echarts-for-react';
import axios from 'axios';
import { CircularProgress } from '@mui/material';
import * as d3 from 'd3-array';

type UUID = string;

interface KeyMoment {
    xvalue: number;
    yvalue: number;
    what: string;
    when: string;
    thoughts: string;
    feelings: string;
    actions: string;
    consequences: string;
}

interface Curve {
    id: UUID;
    data: number[];
    keyMoments?: KeyMoment[];
}

interface SessionSummaryProps {
    sessionId: UUID;
}

const POINTS_COUNT = 150;

const initializeXData = () => {
    const xData: number[] = [];
    const step = 100 / (POINTS_COUNT - 1);
    for (let i = 0; i < POINTS_COUNT; i++) {
        xData.push(i * step);
    }
    return xData;
};

export const SessionSummary: React.FC<SessionSummaryProps> = ({ sessionId }) => {
    const [curves, setCurves] = useState<Curve[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');

    const xData = useMemo(() => initializeXData(), []);

    useEffect(() => {
        const fetchCurvesAndKeyMoments = async () => {
            if (!token) {
                console.error("No authentication token found");
                return;
            }

            try {
                const headers = {
                    Authorization: `Bearer ${token}`,
                };

                const curveResponse = await axios.get(`/api/sessions/${sessionId}/curves`, { headers });
                const fetchedCurves = curveResponse.data;

                const curvesWithKeyMoments = await Promise.all(
                    fetchedCurves.map(async (curve: Curve) => {
                        const keyMomentsResponse = await axios.get(`/api/curves/${curve.id}/keymoments`, { headers });
                        return {
                            ...curve,
                            keyMoments: keyMomentsResponse.data,
                        };
                    })
                );

                setCurves(curvesWithKeyMoments);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching session data:', error);
                setLoading(false);
            }
        };

        fetchCurvesAndKeyMoments();
    }, [sessionId, token]);

    const calculateAverageAndStdDev = (curves: Curve[]) => {
        if (!curves.length) return { avgCurve: [], upperBound: [], lowerBound: [] };

        const yValuesByXIndex: number[][] = Array(POINTS_COUNT).fill(null).map(() => []);

        // Collect y-values by x-index across all curves
        curves.forEach(curve => {
            curve.data.forEach((y, idx) => {
                yValuesByXIndex[idx].push(y);
            });
        });

        // Calculate average and standard deviation for each x-index
        const avgCurve = yValuesByXIndex.map(values => d3.mean(values) || 0);
        const upperBound = yValuesByXIndex.map((values, idx) => avgCurve[idx] + (d3.deviation(values) || 0));
        const lowerBound = yValuesByXIndex.map((values, idx) => avgCurve[idx] - (d3.deviation(values) || 0));

        return { avgCurve, upperBound, lowerBound };
    };

    const { avgCurve, upperBound, lowerBound } = useMemo(() => calculateAverageAndStdDev(curves), [curves]);

    const getOption = useMemo(() => {
        return {
            legend: {
                data: [
                    ...curves.map((_, index) => `Response ${index + 1}`),
                    'Average',
                    'Standard Deviation Area',
                ],
                selectedMode: 'multiple',
            },
            xAxis: {
                type: 'value',
                min: 0,
                max: 100,
                interval: 12.5,
                axisLabel: {
                    formatter: (value: number) => {
                        if (value === 12.5) return 'Before';
                        if (value === 50) return 'During';
                        if (value === 87.5) return 'After';
                        return '';
                    },
                },
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 100,
                name: 'Learning Intensity',
                interval: 25,
                axisLabel: {
                    formatter: (value: number) => {
                        if (value === 25) return 'Low';
                        if (value === 50) return 'Medium';
                        if (value === 75) return 'High';
                        return '';
                    },
                },
            },
            series: [
                // Average curve
                {
                    name: 'Average',
                    type: 'line',
                    data: avgCurve.map((yValue, idx) => [xData[idx], yValue]),
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        width: 2,
                        color: 'blue',
                    },
                    z: 1,
                },
                // Standard deviation area
                {
                    name: 'Standard Deviation Area',
                    type: 'line',
                    data: upperBound.map((yValue, idx) => [xData[idx], yValue]).concat(
                        lowerBound.map((yValue, idx) => [xData[POINTS_COUNT - idx - 1], yValue])
                    ),
                    smooth: true,
                    lineStyle: { opacity: 0 }, // Hide the line
                    areaStyle: {
                        color: 'rgba(0, 0, 255, 0.2)',
                    },
                    z: 0,
                },
                // Response curves
                ...curves.map((curve, index) => ({
                    name: `Response ${index + 1}`,
                    type: 'line',
                    data: curve.data.map((yValue, idx) => [xData[idx], yValue]),
                    smooth: true,
                    showSymbol: false,
                    lineStyle: {
                        width: 2,
                    },
                })),
                // Key Moments as scatter points
                ...curves.map((curve, index) => ({
                    name: `Response ${index + 1}`,
                    type: 'scatter',
                    data: curve.keyMoments?.map((moment) => [moment.xvalue, moment.yvalue]) || [],
                    symbolSize: 10,
                    itemStyle: {
                        color: 'red',
                    },
                    z: 10,
                    label: {
                        show: true,
                        formatter: (params: any) => {
                            const moment = curve.keyMoments?.find(p => p.xvalue === params.data[0] && p.yvalue === params.data[1]);
                            if (!moment) return '';

                            const maxLength = 20;
                            if (moment.what.length > maxLength) {
                                return moment.what.substring(0, maxLength) + '...';
                            }
                            return moment.what;
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
                })),
                // Vertical markers for sections
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
            tooltip: {
                trigger: 'item',
                formatter: (params: any) => {
                    const moment = curves
                        .flatMap(curve => curve.keyMoments || [])
                        .find(point => point.xvalue === params.data[0] && point.yvalue === params.data[1]);
                    if (!moment) return '';

                    return `
                        <div><strong>${moment.what}</strong></div>
                        <div><strong>When:</strong> ${moment.when}</div>
                        <div><strong>Thoughts:</strong> ${moment.thoughts}</div>
                        <div><strong>Feelings:</strong> ${moment.feelings}</div>
                        <div><strong>Actions Taken:</strong> ${moment.actions}</div>
                        <div><strong>Consequences:</strong> ${moment.consequences}</div>
                    `;
                },
            },
        };
    }, [curves, avgCurve, upperBound, lowerBound, xData]);

    return (
        <>
            {loading ? (
                <CircularProgress />
            ) : (
                <ReactEcharts option={getOption} style={{ width: '100%', height: '400px' }} />
            )}
        </>
    );
};
