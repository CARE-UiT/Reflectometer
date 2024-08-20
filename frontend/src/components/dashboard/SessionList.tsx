import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Collapse from '@mui/material/Collapse';
import Box from '@mui/material/Box';
import { Session, createSession, deleteSession, getSessions } from '../../api/sessionList';
import { UserContext } from '../../contexts/user';
import { SessionSummary } from './SessionSummary';

interface SessionListProps {
    course: number;
}
type UUID = string;

const BASE_URL = window.location.origin;

export default function SessionList({ course }: SessionListProps) {
    const { user } = React.useContext(UserContext); // Get user info and token
    const [sessions, setSessions] = React.useState<Session[]>([]);
    const [newSessionName, setNewSessionName] = React.useState('');
    const [isAdding, setIsAdding] = React.useState(false);
    const [expandedSessionId, setExpandedSessionId] = React.useState<UUID | null>(null);

    React.useEffect(() => {
        const fetchSessions = async () => {
            if (user) {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                if (token) {
                    const sessions = await getSessions(token, course);
                    setSessions(sessions);
                }
            }
        };

        fetchSessions();
    }, [course, user]);

    const handleAddClick = async () => {
        if (newSessionName.trim() !== '') {
            try {
                const token = localStorage.getItem('token') || sessionStorage.getItem('token');
                if (token) {
                    const newSession = await createSession(token, course, newSessionName);
                    setSessions((prevSessions) => [...prevSessions, newSession]);
                }
            } catch (error) {
                console.error('Failed to create session:', error);
            } finally {
                setNewSessionName('');
                setIsAdding(false);
            }
        }
    };

    const handleDeleteSession = async (sessionId: UUID) => {
        try {
            const token = localStorage.getItem('token') || sessionStorage.getItem('token');
            if (token) {
                await deleteSession(token, sessionId);
                setSessions((prevSessions) =>
                    prevSessions.filter((session) => session.id !== sessionId)
                );
            }
        } catch (error) {
            console.error('Failed to delete session:', error);
        }
    };

    const handleExpandClick = (sessionId: UUID) => {
        setExpandedSessionId((prevId) => (prevId === sessionId ? null : sessionId));
    };

    return (
        <>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell />
                        <TableCell>Name</TableCell>
                        <TableCell>URL</TableCell>
                        <TableCell align="right">Responses</TableCell>
                        <TableCell align="right">Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {sessions.map((session) => (
                        <React.Fragment key={session.id}>
                            <TableRow>
                                <TableCell>
                                    <IconButton
                                        aria-label="expand row"
                                        size="small"
                                        onClick={() => handleExpandClick(session.id)}
                                    >
                                        <ExpandMoreIcon
                                            style={{
                                                transform:
                                                    expandedSessionId === session.id
                                                        ? 'rotate(180deg)'
                                                        : 'rotate(0deg)',
                                                transition: 'transform 0.3s',
                                            }}
                                        />
                                    </IconButton>
                                </TableCell>
                                <TableCell>{session.name}</TableCell>
                                <TableCell>
                                    <a href={BASE_URL + `/reflectometer/${session.id}`} target="_blank" rel="noopener noreferrer"
                                        style={{ color: 'blue', textDecoration: 'underline' }}
                                    >
                                        {BASE_URL + `/reflectometer/${session.id}`}
                                    </a>
                                </TableCell>
                                <TableCell align="right">{session.curves.length}</TableCell>
                                <TableCell align="right">
                                    <IconButton onClick={() => handleDeleteSession(session.id)} aria-label="delete">
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell colSpan={6} style={{ paddingBottom: 0, paddingTop: 0 }}>
                                    <Collapse in={expandedSessionId === session.id} timeout="auto" unmountOnExit>
                                        <Box margin={1}>
                                            <SessionSummary sessionId={session.id} />
                                        </Box>
                                    </Collapse>
                                </TableCell>
                            </TableRow>
                        </React.Fragment>
                    ))}
                    {isAdding && (
                        <TableRow>
                            <TableCell />
                            <TableCell>{new Date().toLocaleDateString()}</TableCell>
                            <TableCell>
                                <TextField
                                    fullWidth
                                    placeholder="Enter session name"
                                    value={newSessionName}
                                    onChange={(e) => setNewSessionName(e.target.value)}
                                />
                            </TableCell>
                            <TableCell colSpan={2} align="right">
                                <Button variant="contained" color="primary" onClick={handleAddClick}>
                                    Submit
                                </Button>
                            </TableCell>
                            <TableCell align="right">
                                <Button onClick={() => setIsAdding(false)}>Cancel</Button>
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
            {!isAdding && (
                <Grid container justifyContent="flex-end" sx={{ mt: 2 }}>
                    <Button variant="outlined" onClick={() => setIsAdding(true)}>
                        New Session
                    </Button>
                </Grid>
            )}
        </>
    );
}
